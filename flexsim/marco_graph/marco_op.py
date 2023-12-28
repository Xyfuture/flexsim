from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

from flexsim._graph import Graph
from flexsim._node import Node
from flexsim.marco_graph.marco_tensor import MarcoTensor


class MarcoOp(Node):
    def __init__(self, graph: Graph, name: str,op_type:str, input_nodes: Tuple[Node, ...]):
        super().__init__(graph, name, "marco_op", input_nodes)
        self.op_type = op_type
