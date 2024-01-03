from typing import Tuple

from flexsim._graph import Graph
from flexsim._node import Node


class MicroOp:
    def __init__(self):
        pass


class MicroOpNode(Node):
    def __init__(self,graph:Graph, name:str, input_nodes:Tuple[Node,...],micro_op:MicroOp,
                 *args,**kwargs):
        super().__init__(graph,name,"micro_op",input_nodes)

        self.micro_op = micro_op

        self.args = args
        self.kwargs = kwargs
