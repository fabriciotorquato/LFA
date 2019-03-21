#Depende do matplotlib e do networkx
import networkx as nx
import matplotlib.pyplot as plt
class Graph():
    def __init__(self):
        self.list_edge = []
        self.list_node = []

    def show(self):
        G=nx.Graph()
        G.add_nodes_from(x.name for x in self.list_node)

        for node in self.list_node:
            for edge in node.edges:
                G.add_edge(node.name, edge.node.name)


        print("Nodes do Grafo: ")
        print(G.nodes())
        print("Edges do Grafo: ")
        print(G.edges())

        nx.draw(G)
        plt.savefig("./teste.png") # save as png
        plt.show() # display
