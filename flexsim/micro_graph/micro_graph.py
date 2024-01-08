from typing import Tuple

from flexsim._graph import Graph
from flexsim._node import Node
from flexsim.micro_graph.micro_op import MicroOp, MicroOpNode
from flexsim.micro_graph.micro_tensor import MicroTensor, MicroTensorNode


class MicroGraph(Graph):
    def __init__(self):
        super().__init__()

    def create_op_node(self, name: str, input_nodes: Tuple[Node, ...], micro_op: MicroOp, *args, **kwargs):
        node = MicroOpNode(self, name, input_nodes, micro_op, *args, **kwargs)
        self.add_node(node)

        return node

    def create_tensor_node(self, name: str, input_nodes: Tuple[Node, ...], micro_tensor: MicroTensor, *args, **kwargs):
        node = MicroTensorNode(self, name, input_nodes, micro_tensor, *args, **kwargs)
        self.add_node(node)

        return node

    def check_valid(self) -> bool:
        # check current graph is valid or not
        # micro_tensor -> micro_op -> micro_tensor
        pass
