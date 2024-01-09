from typing import Tuple, Dict, Union, List

from flexsim._graph import Graph
from flexsim._node import Node
import torch

SingleTensorSliceType = Tuple[Union[int, slice], ...]
MultiTensorSliceType = List[SingleTensorSliceType]


class MicroTensor:
    # recording finish time and finish position
    def __init__(self, tensor_shape: Tuple[int, ...]):
        self.tensor_shape = tensor_shape

        self._tensor_position_time: Dict[int, torch.Tensor] = {}

    def get_finish_time(self, slices: Tuple[slice]):
        pass

    def get_finish_position(self, tensor_slice: SingleTensorSliceType) -> List[int]:
        pass

    def get_finish_position_time(self, tensor_slice_list: MultiTensorSliceType) -> List[Tuple[int, int]]:
        """

        :param tensor_slice_list:
        :return: (position, time)
        """
        pass

    def is_data_ready(self, tensor_slices: MultiTensorSliceType) -> bool:
        tmp_time = torch.zeros(self.tensor_shape, dtype=torch.float32)

        for k, v in self._tensor_position_time:
            tmp_time += v
        tmp_time: torch.Tensor = (tmp_time == 0)

        if not tmp_time.any().item():
            return True

        for cur_slice in tensor_slices:
            if tmp_time[cur_slice].any().item():
                return False

        return True

    def set_finish_position_time(self, position: int, time: float, slices: MultiTensorSliceType):
        if position not in self._tensor_position_time:
            # create new tensor and allocate finish time
            # time start at 1 ns
            # if time = 0, means invalid (not in this position)
            self._tensor_position_time[position] = torch.zeros(self.tensor_shape, dtype=torch.float32)

        finish_time_tensor = self._tensor_position_time[position]
        for s in slices:
            finish_time_tensor[s] = time

    def get_max_time(self):
        max_time = 0
        for k, v in self._tensor_position_time.items():
            if torch.max(v) > max_time:
                max_time = torch.max(v)
        return max_time

    def reset(self):
        self._tensor_position_time = {}

    def __getitem__(self, item):
        pass


class MicroTensorNode(Node):
    def __init__(self, graph: Graph, name: str, input_nodes: Tuple[Node, ...], micro_tensor: MicroTensor,
                 *args, **kwargs):
        super().__init__(graph, name, "micro_tensor", input_nodes)

        self.micro_tensor = micro_tensor
        self.args = args
        self.kwargs = kwargs


class MicroTensorFragment:
    def __init__(self, micro_tensor: MicroTensor, tensor_slice_list: MultiTensorSliceType):
        self.micro_tensor = micro_tensor
        self.tensor_slice_list = tensor_slice_list
