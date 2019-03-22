#Depende do matplotlib e do networkx
import networkx as nx
import matplotlib.pyplot as plt
class Graph():
    def __init__(self):
        self.list_edge = []
        self.list_node = []

    def show(self):
        G=nx.DiGraph()
        G.add_nodes_from(x.name for x in self.list_node)
        labels={}
        for node in self.list_node:
            for edge in node.edges:
                labels[(node.name, edge.node.name)] = edge.name
                G.add_edge(node.name, edge.node.name)


        print("Nodes do Grafo: ")
        print(G.nodes())
        print("Edges do Grafo: ")
        print(G.edges())
        print(labels)
        pos = nx.layout.spring_layout(G)
        nx.draw(G, pos, with_labels = True, edge_color='black',width=1,linewidths=1, node_size=500,node_color='green',alpha=0.9,)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

        plt.savefig("./teste.png") # save as png
        plt.show() # display
