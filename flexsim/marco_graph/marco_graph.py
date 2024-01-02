from __future__ import annotations

from typing import Tuple

from flexsim._graph import Graph
from flexsim._node import Node
from flexsim.marco_graph.marco_op import MarcoOp, MarcoOpNode


class MarcoGraph(Graph):
    def __init__(self):
        super().__init__()

    def create_node(self, name: str, op_type: str, input_nodes: Tuple[Node, ...], marco_op: MarcoOp,
                    output_shape: Tuple[int, ...] = (), *args, **kwargs):
        node = MarcoOpNode(self, name, op_type, input_nodes, marco_op)
        self.add_node(node)
