import torch

from flexsim.macro_graph.macro_op import MacroOp


class ReLU(MacroOp):
    def __init__(self):
        super().__init__()

    @staticmethod
    def create_from_torch(torch_op: torch.nn.ReLU):
        assert isinstance(torch_op, torch.nn.ReLU)

        return ReLU()
