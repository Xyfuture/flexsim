from flexsim.graph import Graph


class MarcoGraph(Graph):
    def __init__(self):
        super().__init__()

        self.nodes = []
        self.edges = []