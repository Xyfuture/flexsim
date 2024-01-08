from typing import Tuple

from flexsim._graph import Graph
from flexsim._node import Node
import torch


class MicroTensor:
    # recording finish time and finish position
    def __init__(self, tensor_shape: Tuple[int, ...]):
        self.tensor_shape = tensor_shape

        self.finish_time = torch.zeros(self.tensor_shape, dtype=torch.int32)
        self.finish_position = torch.zeros(self.tensor_shape, dtype=torch.int16)

    def get_finish_time(self):
        pass

    def get_finish_position(self):
        pass

    def set_finish_time(self):
        pass

    def set_finish_position(self):
        pass

    def get_max_time(self):
        return torch.max(self.finish_time)

    def reset(self):
        self.finish_time = torch.zeros(self.tensor_shape, dtype=torch.int32)
        self.finish_position = torch.zeros(self.tensor_shape, dtype=torch.int16)

class MicroTensorNode(Node):
    def __init__(self, graph: Graph, name: str, input_nodes: Tuple[Node, ...], micro_tensor: MicroTensor,
                 *args, **kwargs):
        super().__init__(graph, name, "micro_tensor", input_nodes)

        self.micro_tensor = micro_tensor
        self.args = args
        self.kwargs = kwargs
