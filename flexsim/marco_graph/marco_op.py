from __future__ import annotations

import operator
from abc import ABC, abstractmethod
from typing import Tuple, Union

import torch
import torch.nn as nn

from flexsim._graph import Graph
from flexsim._node import Node
from flexsim.marco_graph.marco_tensor import MarcoTensor
from marco_ops import *


class MarcoOp:
    def __init__(self):
        pass

    @staticmethod
    def create_from_torch(torch_op):
        return None


class MarcoOpNode(Node):
    def __init__(self, graph: Graph, name: str, input_nodes: Tuple[Node, ...], marco_op: MarcoOp,
                 output_shape: Tuple[int, ...] = (),
                 *args, **kwargs):
        super().__init__(graph, name, "marco_op", input_nodes)

        self.marco_op = marco_op
        self.output_shape = output_shape

        self.args = args
        self.kwargs = kwargs


def create_marco_op_from_torch(torch_op)->MarcoOp:
    if isinstance(torch_op,nn.Conv2d):
        return Conv2d.create_from_torch(torch_op)
    elif isinstance(torch_op,nn.Linear):
        return Linear.create_from_torch(torch_op)
    elif isinstance(torch_op,nn.MaxPool2d):
        return MaxPool2d.create_from_torch(torch_op)
    elif isinstance(torch_op,nn.AvgPool2d):
        return AvgPool2d.create_from_torch(torch_op)
    elif torch_op is operator.add:
        return Add()
    elif torch_op is torch.flatten:
        return Flatten()
    pass
