from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple, Union

import torch

from flexsim._graph import Graph
from flexsim._node import Node
from flexsim.marco_graph.marco_tensor import MarcoTensor




class MarcoOp:
    def __init__(self):
        pass


class MarcoOpNode(Node):
    def __init__(self, graph: Graph, name: str, op_type: str, input_nodes: Tuple[Node, ...], marco_op: MarcoOp,
                 output_shape: Tuple[int, ...] = (),
                 *args, **kwargs):
        super().__init__(graph, name, "marco_op", input_nodes)
        self.op_type = op_type
        self.marco_op = marco_op

        self.args = args
        self.kwargs = kwargs



def get_torch_node_callable(torch_node:torch.fx.Node):
    if torch_node.op == 'call_method':
        pass
    elif torch_node.op == 'call_module':
        pass
    elif torch_node.op == 'call_function':
        pass
    else:
        # placeholder get_attr output <- op_type
        raise RuntimeError("Unsupported op type")

