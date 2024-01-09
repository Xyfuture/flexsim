from typing import Tuple

from flexsim.macro_graph.macro_op import MacroOp


class InputNode(MacroOp):
    def __init__(self, input_shape: Tuple[int]):
        super().__init__()
        self.input_shape = input_shape


class OutputNode(MacroOp):
    def __init__(self):
        super().__init__()
