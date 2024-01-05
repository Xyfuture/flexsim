from typing import Tuple, List

from flexsim._graph import Graph
from flexsim._node import Node
from flexsim.hardware_base import HardwareBase
from flexsim.machine_op import MachineOp


class Operation:
    """
    describe an operation on tensor
    used in micro op
    """

    def __init__(self, machine_op: MachineOp, input_slices: Tuple[slice, ...], output_slices: Tuple[slice, ...]):
        self.machine_op = machine_op
        self.input_slices = input_slices
        self.output_slices = output_slices


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
