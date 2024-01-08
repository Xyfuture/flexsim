from typing import Tuple, List

from flexsim._graph import Graph
from flexsim._node import Node
from flexsim.hardware_base import HardwareBase
from flexsim.machine_op import MachineOp
from flexsim.micro_graph.micro_tensor import MicroTensor


class MicroTensorSlice:
    def __init__(self, micro_tensor: MicroTensor, tensor_slices: Tuple[slice]):
        self.micro_tensor = micro_tensor
        self.tensor_slices = tensor_slices


class Operation:
    """
    describe an operation on tensor
    used in micro op
    """

    def __init__(self, machine_op: MachineOp, input_slices: Tuple[MicroTensorSlice, ...],
                 output_slices: Tuple[MicroTensorSlice, ...],*args,**kwargs):
        self.machine_op = machine_op
        self.input_slices = input_slices
        self.output_slices = output_slices

        self.args = args
        self.kwargs = kwargs


class MicroOp:
    """
    A micro op represent a collection of operations on the same hardware component,
    which are unrolled form a loop-based marco op and shares the same input and output.
    """

    def __init__(self, component: HardwareBase, op: str, ):
        self.component = component
        self.op = op

        self.operation_list: List[Operation] = []


class MicroOpNode(Node):
    def __init__(self, graph: Graph, name: str, input_nodes: Tuple[Node, ...], micro_op: MicroOp,
                 *args, **kwargs):
        super().__init__(graph, name, "micro_op", input_nodes)

        self.micro_op = micro_op

        self.args = args
        self.kwargs = kwargs
