from __future__ import annotations

from typing import Tuple

from flexsim._graph import Graph
from flexsim._node import Node


class MarcoTensor(Node):
    def __init__(self, graph: Graph, name: str, tensor_shape: tuple[int], input_nodes: Tuple[Node, ...]):
        super().__init__(graph, name, "marco_tensor", input_nodes)
        self.tensor_shape = tensor_shape
