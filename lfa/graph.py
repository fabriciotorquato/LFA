# Depende do matplotlib e do networkx
import networkx as nx
import matplotlib.pyplot as plt


class Graph():
    def __init__(self):
        self.node_init = None
        self.list_edge = []
        self.list_node = []
        self.node_finals = []
        self.node_name = 0
        self.state_name = 0

    def getNextName(self):
        self.node_name += 1
        return self.node_name

    def getNextState(self):
        self.state_name += 1
        return 'S{}'.format(self.state_name)

    def addNodes(self, nodes):
        [self.list_node.append(node) for node in nodes]

    def findNode(self, name):
        for node in self.list_node:
            if node.name == name:
                return node
        return None

    def addEdges(self, edges):
        for edge in edges:
            if edge in self.list_edge:
                return False
            self.list_edge.append(edge)
        return True

    def show(self):

        G = nx.OrderedMultiDiGraph()
        G.add_nodes_from(x.name for x in self.list_node)

        labels = {}

        for node in self.list_node:
            for edge in node.edges:
                labels[(node.name, edge.node.name)] = edge.name
                G.add_edge(node.name, edge.node.name, length=5)

        print("Nodes do Grafo Inicial: ")
        print(self.node_init.name)
        print("Nodes do Grafo Finais: ")
        [print(node) for node in self.node_finals]
        print("Nodes do Grafo: ")
        print(G.nodes())
        print("Edges do Grafo: ")
        print(G.edges())
        print(labels)

        pos = nx.layout.spring_layout(G)

        plt.figure(figsize=(20, 20))

        nx.draw(G, pos, with_labels=True, edge_color='black', width=2,
                linewidths=1, node_size=250, node_color='green', alpha=0.9,)

        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.savefig("../graph.png")  # save as png
        plt.show()  # display
