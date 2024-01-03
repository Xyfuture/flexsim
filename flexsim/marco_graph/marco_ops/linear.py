import torch.nn

from flexsim.marco_graph.marco_op import MarcoOp


class Linear(MarcoOp):
    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        super().__init__()

        self.in_features = in_features
        self.out_features = out_features
        self.bias = bias

    @staticmethod
    def create_from_torch(torch_op: torch.nn.Linear):
        assert isinstance(torch_op, torch.nn.Linear)

        in_features = torch_op.in_features
        out_features = torch_op.out_features
        bias = True if torch_op.bias else False

        return Linear(in_features,out_features,bias)

