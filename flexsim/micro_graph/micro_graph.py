from flexsim._graph import Graph


class MicroGraph(Graph):
    def __init__(self):
        super().__init__()

    def create_node(self):
        # two types of node MicroTensorNode and MicroOpNode
        pass