import torch

from flexsim.marco_graph.marco_op import MarcoOp


class ReLU(MarcoOp):
    def __init__(self):
        super().__init__()

    @staticmethod
    def create_from_torch(torch_op: torch.nn.ReLU):
        assert isinstance(torch_op, torch.nn.ReLU)

        return ReLU()
