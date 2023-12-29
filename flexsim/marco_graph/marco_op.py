from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

from flexsim._graph import Graph
from flexsim._node import Node
from flexsim.marco_graph.marco_tensor import MarcoTensor


class MarcoOp:
    def __init__(self):
        pass


class MarcoOpNode(Node):
    def __init__(self, graph: Graph, name: str, op_type: str, input_nodes: Tuple[Node, ...], marco_op: MarcoOp,
                 *args, **kwargs):
        super().__init__(graph, name, "marco_op", input_nodes)
        self.op_type = op_type
        self.marco_op = marco_op

        self.args = args
        self.kwargs = kwargs
