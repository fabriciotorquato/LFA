class DFAedge():
    def __init__(self, name):
        self.name = name
        self.nodes_name = ''
        self.nodes = []
        self.edges = []

    def getStringSolution(self):
        self.nodes_name = '|'.join(
            [str(item.name) for item in self.nodes])
        return self.nodes_name
