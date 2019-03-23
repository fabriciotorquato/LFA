# Depende do matplotlib e do networkx
import networkx as nx
import matplotlib.pyplot as plt


class Graph():
    def __init__(self):
        self.list_edge = []
        self.list_node = []
        self.node_name = 0

    def getNextName(self):
        self.node_name += 1
        return self.node_name

    def addNodes(self, nodes):
        for node in nodes:
            self.list_node.append(node)

    def addEdges(self, edges):
        for edge in edges:
            self.list_edge.append(edge)

    def show(self):
        G = nx.OrderedMultiDiGraph()
        G.add_nodes_from(x.name for x in self.list_node)
        labels = {}
        for node in self.list_node:
            for edge in node.edges:
                labels[(edge.node.name, node.name)] = edge.name
                G.add_edge(edge.node.name, node.name, length=5)

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

        plt.savefig("./teste.png")  # save as png
        plt.show()  # display
