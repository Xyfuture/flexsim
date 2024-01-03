from typing import Tuple

import torch.nn

from flexsim.marco_graph.marco_op import MarcoOp


class MaxPool2d(MarcoOp):
    def __init__(self, kernel_size: Tuple[int, int], stride: Tuple[int, int] = (1, 1), padding: int = 0):
        super().__init__()
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding

    @staticmethod
    def create_from_torch(torch_op: torch.nn.MaxPool2d):
        assert isinstance(torch_op, torch.nn.MaxPool2d)
        kernel_size = torch_op.kernel_size
        stride = torch_op.stride
        padding = torch_op.padding

        if isinstance(kernel_size, int):
            kernel_size = (kernel_size, kernel_size)
        if isinstance(stride, int):
            stride = (stride, stride)

        return MaxPool2d(kernel_size, stride, padding)


class AvgPool2d(MarcoOp):
    def __init__(self, kernel_size: Tuple[int, int], stride: Tuple[int, int] = (1, 1), padding: int = 0):
        super().__init__()
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding

    @staticmethod
    def create_from_torch(torch_op: torch.nn.AvgPool2d):
        assert isinstance(torch_op, torch.nn.AvgPool2d)
        kernel_size = torch_op.kernel_size
        stride = torch_op.stride
        padding = torch_op.padding

        if isinstance(kernel_size, int):
            kernel_size = (kernel_size, kernel_size)
        if isinstance(stride, int):
            stride = (stride, stride)

        return AvgPool2d(kernel_size, stride, padding)
