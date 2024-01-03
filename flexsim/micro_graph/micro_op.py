from typing import Tuple

from flexsim._graph import Graph
from flexsim._node import Node


class MicroOp:
    """
    A micro op represent a collection of operations on the same hardware component,
    which are unrolled form a loop-based marco op and shares the same input and output.
    """
    def __init__(self):
        pass


class MicroOpNode(Node):
    def __init__(self,graph:Graph, name:str, input_nodes:Tuple[Node,...],micro_op:MicroOp,
                 *args,**kwargs):
        super().__init__(graph,name,"micro_op",input_nodes)

        self.micro_op = micro_op

        self.args = args
        self.kwargs = kwargs
