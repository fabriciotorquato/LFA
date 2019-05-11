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

    def getjokerState(self):
        return 'S99'

    def addNodes(self, nodes):
        [self.list_node.append(node) for node in nodes]

    def removeNode(self, node_name):
        edges_in = []
        edges_out = []
        is_final_node = False
        is_initial_node = False

        for node in self.list_node:
            if node.name == node_name:
                edges_out = node.edges
                is_final_node = node.is_final_node
                is_initial_node = node.is_initial_node
                self.list_node.remove(node)

        for edge in self.list_edge:
            if edge.node.name == node_name:
                edges_in.append(edge)

        return edges_in, edges_out, is_final_node, is_initial_node

    def removeJoker(self):
        node_name = self.getjokerState()

        for node in self.list_node:
            list_edges_removed = []
            for edge in node.edges:
                if node_name == edge.node.name:
                    list_edges_removed.append(edge)
                    self.list_edge.remove(edge)
            for edge in list_edges_removed:
                node.edges.remove(edge)

        for node in self.list_node:
            if node_name == node.name:
                self.list_node.remove(node)

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

    def findEdgeCaracter(self, node_name, caracter):
        for node in self.list_node:
            if node.name == node_name:
                for edge in node.edges:
                    if edge.name == caracter:
                        return edge.node
        return None

    def show(self):

        G = nx.OrderedMultiDiGraph()
        G.add_nodes_from(x.name for x in self.list_node)

        labels = {}

        for node in self.list_node:
            for edge in node.edges:
                # Fazer o graico ser aceito pra edges do mesmo ponto
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
        print("Labels do Grafo: ")
        print(labels)
        # labels={}

        pos = nx.layout.spring_layout(G)

        plt.figure(figsize=(20, 20))

        nx.draw(G, pos, with_labels=True, edge_color='black', width=2,
                linewidths=1, node_size=250, node_color='green', alpha=0.9,)

        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.savefig("../graph.png")  # save as png
        plt.show()  # display
