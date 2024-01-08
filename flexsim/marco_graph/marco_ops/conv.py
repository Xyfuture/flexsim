from __future__ import annotations

from typing import Tuple

import torch

from flexsim.marco_graph.marco_op import MarcoOp


class Conv2d(MarcoOp):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: Tuple[int, int], stride: Tuple[int,int] = (1,1),
                 padding: int = 0, bias: bool = True,
                 *args, **kwargs):
        super().__init__()

        # keep the same with torch.nn.Conv2d
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.bias = bias

        self.kernel_shape = (out_channels, kernel_size[0], kernel_size[1], in_channels)

        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def create_from_torch(torch_module: torch.nn.Conv2d):
        assert isinstance(torch_module, torch.nn.Conv2d)

        in_channels = torch_module.in_channels
        out_channels = torch_module.out_channels
        kernel_size = torch_module.kernel_size
        stride = torch_module.stride
        padding = torch_module.padding
        bias = True if torch_module.bias else False

        if isinstance(kernel_size,int):
            kernel_size = (kernel_size, kernel_size)

        if isinstance(stride,int):
            stride = (stride, stride)

        if isinstance(padding,str):
            padding = int(padding)

        return Conv2d(in_channels, out_channels, kernel_size, stride, padding,bias)