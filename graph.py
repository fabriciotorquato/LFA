# Depende do matplotlib e do networkx
import networkx as nx
import matplotlib.pyplot as plt


class Graph():
    def __init__(self):
        self.list_edge = []
        self.list_node = []
        self.node_name = 0
        self.state_name = 0

    def getNextName(self):
        self.node_name += 1
        return self.node_name

    def getNextState(self):
        self.state_name += 1
        return 'S{}'.format(self.state_name)

    def getCurrentState(self):
        return 'S{}'.format(self.state_name)

    def addNodes(self, nodes):
        for node in nodes:
            self.list_node.append(node)

    def findNode(self, name):
        for node in self.list_node:
            if node.name == name:
                return node
        return None

    def getStringSolution(self, solution):
        string_solution = ''.join(
            [str(item.name) for item in solution])
        return string_solution

    def addEdges(self, edges):
        for edge in edges:
            if edge not in self.list_edge:
                self.list_edge.append(edge)
            else:
                return False
        return True

    def clearNodes(self):
        is_nodes_validaded = True

        while is_nodes_validaded:
            new_node_list = []
            new_edge_list = set()
            is_nodes_validaded = False
            for node in self.list_node:
                validaded = False
                for edge in self.list_edge:
                    if node.name == edge.node.name:
                        if not (len(node.edges) == 1 and node.edges[0].node.name == node.name):
                            new_edge_list.add(edge)
                            validaded = True
                if validaded:
                    new_node_list.append(node)
                else:
                    is_nodes_validaded = True
            self.list_edge = list(new_edge_list)
            print(len(self.list_edge))
            self.list_node = new_node_list
            print(len(self.list_node))

    def show(self):
        G = nx.OrderedMultiDiGraph()
        G.add_nodes_from(x.name for x in self.list_node)
        labels = {}
        for node in self.list_node:
            for edge in node.edges:
                labels[(node.name, edge.node.name)] = edge.name
                G.add_edge(node.name, edge.node.name, length=5)

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
