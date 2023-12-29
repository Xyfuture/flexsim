from __future__ import annotations

from typing import Tuple

from flexsim._graph import Graph
from flexsim._node import Node


class MarcoTensor:
    def __init__(self):
        pass


class MarcoTensorNode(Node):
    def __init__(self, graph: Graph, name: str, input_nodes: Tuple[Node, ...], marco_tensor: MarcoTensor):
        super().__init__(graph, name, "marco_tensor", input_nodes)
        self.marco_tensor = marco_tensor
