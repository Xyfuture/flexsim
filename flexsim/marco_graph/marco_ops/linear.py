from flexsim.marco_graph.marco_op import MarcoOp


class Linear(MarcoOp):
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()

        self.in_features = in_features
        self.out_features = out_features
        self.bias = bias
