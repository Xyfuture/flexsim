from __future__ import annotations

from typing import Tuple

from flexsim._graph import Graph
from flexsim._node import Node
from flexsim.macro_graph.macro_op import MacroOp, MacroOpNode


class MacroGraph(Graph):
    def __init__(self):
        super().__init__()

    def create_node(self, name: str, input_nodes: Tuple[Node, ...], macro_op: MacroOp,
                    output_shape: Tuple[int, ...] = (), *args, **kwargs):
        node = MacroOpNode(self, name, input_nodes, macro_op, output_shape, *args, **kwargs)
        self.add_node(node)

        return node
