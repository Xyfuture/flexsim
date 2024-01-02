from typing import Tuple

from flexsim.marco_graph.marco_op import MarcoOp


class InputNode(MarcoOp):
    def __init__(self, input_shape: Tuple[int]):
        super().__init__()
        self.input_shape = input_shape

