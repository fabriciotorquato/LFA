class Graph():
    def __init__(self):
        self.list_edge = []
        self.list_node = []

    def show(self):
        for node in self.list_node:

            print("\n", node.name)
            if node.edge:
                print(node.edge.name)
            if node.edge and node.edge.node:
                print(node.edge.node.name,"\n")