from __future__ import annotations
from typing import Tuple, Dict, List
from collections import deque
import torch
import torch.nn as nn
import torch.fx as fx
from torch.fx.passes.shape_prop import ShapeProp
from flexsim.marco_graph.marco_graph import MarcoGraph
from flexsim.marco_graph.marco_ops.misc import InputNode
from flexsim.marco_graph.marco_tensor import MarcoTensor


class _TopoNode:
    def __init__(self, torch_node: fx.Node):
        self.torch_node = torch_node

    def __hash__(self):
        return self.torch_node.__hash__()

    def __eq__(self, other: _TopoNode):
        return self.torch_node == other.torch_node


class MarcoParser:
    def __init__(self, torch_graph_module: fx.GraphModule, input_shape: Tuple[int]):
        self.input_shape = input_shape
        self.torch_graph_module: torch.fx.GraphModule = torch_graph_module
        self.torch_graph: torch.fx.Graph = self.torch_graph_module.graph
        self.marco_graph = MarcoGraph()

    def make_marco_graph(self):
        # create input node
        self.marco_graph.create_node("input", "input", (), InputNode(self.input_shape), self.input_shape)

        # use toposort build new marco graph.
        # build tmp proxy graph
        topo_node_map: Dict[fx.Node, _TopoNode] = {}
        output_dep_graph: Dict[_TopoNode, List[_TopoNode, ...]] = {}
        input_dep_num:Dict[_TopoNode,int] = {}
        sorted_graph = []

        torch_node: fx.Node
        for torch_node in self.marco_graph.nodes:
            topo_node_map[torch_node] = _TopoNode(torch_node)

        torch_node: fx.node
        for torch_node in self.marco_graph.nodes:
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
        for k,v in input_dep_num.items():
            if v == 0:
                zero_dep_queue.append(k)
        while len(zero_dep_queue):
            cur_topo_node:_TopoNode = zero_dep_queue.pop()
            sorted_graph.append(cur_topo_node)
            for successor in output_dep_graph[cur_topo_node]:
                input_dep_num[successor] -= 1
                if input_dep_num[successor] == 0:
                    zero_dep_queue.append(successor)

        # build finish

        # create marco graph
        for topo_node in sorted_graph:
            torch_node = topo_node.torch_node


    def build_op_node(self,torch_node:fx.node):
        pass


    def tensor_shape_inference(self):
        random_input = torch.randn(self.input_shape)
        ShapeProp(self.torch_graph_module).propagate(random_input)
