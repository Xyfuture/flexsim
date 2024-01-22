from __future__ import annotations

from collections import deque
from typing import Tuple, Dict, List

import torch
import torch.fx as fx
from torch.fx.passes.shape_prop import ShapeProp

from flexsim.macro_graph.macro_graph import MacroGraph
from flexsim.macro_graph.macro_op import create_macro_op_from_torch, MacroOp, MacroOpNode
from flexsim.macro_graph.macro_ops.misc import InputNode, OutputNode


class _TopoNode:
    def __init__(self, torch_node: fx.Node):
        self.torch_node = torch_node

    def __hash__(self):
        return self.torch_node.__hash__()

    def __eq__(self, other: _TopoNode):
        return self.torch_node == other.torch_node


class MacroParser:
    def __init__(self, torch_graph_module: fx.GraphModule, input_shape: Tuple[int]):
        self.input_shape = input_shape
        self.torch_graph_module: torch.fx.GraphModule = torch_graph_module
        self.torch_modules_dict = dict(self.torch_graph_module.named_modules())
        self.torch_graph: torch.fx.Graph = self.torch_graph_module.graph
        self.macro_graph = MacroGraph()

    def make_macro_graph(self):
        # create input node
        self.macro_graph.create_node("input", (), InputNode(self.input_shape), self.input_shape)

        # use toposort build new macro graph.
        # build tmp proxy graph
        topo_node_map: Dict[fx.Node, _TopoNode] = {}
        output_dep_graph: Dict[_TopoNode, List[_TopoNode]] = {}
        input_dep_num: Dict[_TopoNode, int] = {}
        sorted_graph = []

        torch_node: fx.Node
        for torch_node in self.macro_graph.nodes:
            topo_node_map[torch_node] = _TopoNode(torch_node)

        torch_node: fx.node
        for torch_node in self.macro_graph.nodes:
            user_node: fx.node
            for user_node in torch_node.users.keys():
                predecessor, successor = topo_node_map[torch_node], topo_node_map[user_node]
                if predecessor in output_dep_graph:
                    output_dep_graph[predecessor].append(successor)
                else:
                    output_dep_graph[predecessor] = [successor]

                if successor in input_dep_num:
                    input_dep_num[successor] += 1
                else:
                    input_dep_num[successor] = 1

        # run toposort on proxy graph
        zero_dep_queue = deque()
        for k, v in input_dep_num.items():
            if v == 0:
                zero_dep_queue.append(k)
        while len(zero_dep_queue):
            cur_topo_node: _TopoNode = zero_dep_queue.popleft()
            sorted_graph.append(cur_topo_node)
            for successor in output_dep_graph[cur_topo_node]:
                input_dep_num[successor] -= 1
                if input_dep_num[successor] == 0:
                    zero_dep_queue.append(successor)

        # build finish

        # create macro graph
        macro_node_map: Dict[fx.Node, MacroOpNode] = {}
        for topo_node in sorted_graph:
            torch_node = topo_node.torch_node
            macro_op = self.build_macro_op_from_torch_node(torch_node)
            output_shape = torch_node.meta['tensor_meta'].shape
            input_nodes = tuple(macro_node_map[node] for node in torch_node.all_input_nodes)
            node_name = torch_node.name

            macro_op_node = self.macro_graph.create_node(node_name, input_nodes, macro_op, output_shape)
            macro_node_map[torch_node] = macro_op_node

    def build_macro_op_from_torch_node(self, torch_node: fx.Node) -> MacroOp:
        node_target = torch_node.target
        target = None

        if torch_node.op == 'call_module':
            target = self.torch_modules_dict[node_target]
        elif torch_node.op == 'call_function':
            target = node_target
        elif torch_node.op == 'output':
            return OutputNode()
        else:
            # placeholder get_attr output call_method <- op_type
            raise RuntimeError("Unsupported op type")

        macro_op = create_macro_op_from_torch(target)
        return macro_op

    def tensor_shape_inference(self):
        random_input = torch.randn(self.input_shape)
        ShapeProp(self.torch_graph_module).propagate(random_input)
