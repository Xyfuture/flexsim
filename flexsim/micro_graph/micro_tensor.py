from typing import Tuple

from flexsim._graph import Graph
from flexsim._node import Node


class MicroTensor:
    # recording finish time and finish position
    def __init__(self):
        pass


class MicroTensorNode(Node):
    def __init__(self, graph: Graph, name: str, input_nodes: Tuple[Node, ...], micro_tensor: MicroTensor,
                 *args, **kwargs):
        super().__init__(graph, name, "micro_tensor", input_nodes)

        self.micro_tensor = micro_tensor
        self.args = args
        self.kwargs = kwargs
