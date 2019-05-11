class DFANode():
    def __init__(self, name, is_final_node=False):
        self.name = name
        self.nodes_name = ''
        self.nodes = []
        self.edges = []
        self.is_final_node = is_final_node

    def convertStringSolution(self):
        self.nodes.sort(key=lambda x: x.name)
        self.nodes_name = '|'.join(
            [str(item.name) for item in self.nodes])
        return self.nodes_name
