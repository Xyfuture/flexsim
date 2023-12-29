from __future__ import annotations

from typing import Tuple

from flexsim._node import Node
from flexsim.marco_graph.marco_op import MarcoOp
from flexsim._graph import Graph


class Conv2d(MarcoOp):
    def __init__(self, graph: Graph, name: str, input_nodes: Tuple[Node, ...],
                 in_channels, out_channels, kernel_size, stride=1, padding=0, bias=True,
                 *args, **kwargs):
        super().__init__(graph, name, "conv2d", input_nodes)

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


