from flexsim.marco_graph.marco_op import MarcoOp


class MaxPooling2d(MarcoOp):
    def __init__(self,kernel_size,stride=1,padding=0):
        super().__init__()
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding


