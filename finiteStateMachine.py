#!/usr/bin/python
# -*- coding: utf-8 -*-

from edge import Edge
from node import Node
from graph import Graph


class FiniteStateMachine():
    def __init__(self, postfixNotation):
        self.postfixNotation = postfixNotation
        self.graph = Graph()
        self.queue = []

    def addNodeAnd(self):
        first_node_0, second_node_0 = self.queue.pop()
        first_node_1, second_node_1 = self.queue.pop()

        edge_1 = Edge(first_node_1, '&')
        second_node_0.edges.append(edge_1)

        init_node = Node(self.graph.getNextName())
        edge_2 = Edge(first_node_0, '&')
        init_node.edges.append(edge_2)

        final_node = Node(self.graph.getNextName())
        edge_3 = Edge(final_node, '&')
        second_node_1.edges.append(edge_3)

        self.graph.addNodes([init_node, final_node])

        self.graph.addEdges([edge_1, edge_2, edge_3])

        self.queue.append((init_node, final_node))

    def addNodeOr(self):
        first_node_1, second_node_1 = self.queue.pop()
        first_node_0, second_node_0 = self.queue.pop()

        init_node = Node(self.graph.getNextName())

        edge_node_1 = Edge(first_node_1, '&')
        edge_node_2 = Edge(first_node_0, '&')

        init_node.edges.append(edge_node_1)
        init_node.edges.append(edge_node_2)

        final_node = Node(self.graph.getNextName())

        edge_node_3 = Edge(final_node, '&')
        edge_node_4 = Edge(final_node, '&')

        second_node_1.edges.append(edge_node_3)
        second_node_0.edges.append(edge_node_4)

        self.graph.addNodes([init_node, final_node])

        self.graph.addEdges(
            [edge_node_1, edge_node_2, edge_node_3, edge_node_4])

        self.queue.append((init_node, final_node))

    def getNodeCloseState(self):
        first_node, second_node = self.queue.pop()

        init_node = Node(self.graph.getNextName())
        final_node = Node(self.graph.getNextName())

        edge_node_1 = Edge(final_node, '&')
        edge_node_2 = Edge(first_node, '&')

        init_node.edges.append(edge_node_1)
        init_node.edges.append(edge_node_2)

        edge_node_3 = Edge(final_node, '&')
        second_node.edges.append(edge_node_3)

        edge_node_4 = Edge(init_node, '&')
        final_node.edges.append(edge_node_4)

        self.graph.addNodes([init_node, final_node])

        self.graph.addEdges(
            [edge_node_1, edge_node_2, edge_node_3, edge_node_4])

        self.queue.append((init_node, final_node))

    def addNodeState(self, caracter):
        edge = Edge(None, caracter)

        fisrt_node = Node(self.graph.getNextName())
        second_node = Node(self.graph.getNextName())

        edge.node = second_node
        fisrt_node.edges.append(edge)

        self.graph.addNodes([fisrt_node, second_node])
        self.graph.addEdges([edge])
        self.queue.append((fisrt_node, second_node))

    def getNFA(self):
        for caracter in self.postfixNotation.expression_postfix:
            if (caracter >= 'A' and caracter <= 'Z' or caracter >= 'a' and caracter <= 'z'):
                self.addNodeState(caracter)
            elif caracter == '.':
                self.addNodeAnd()
            elif caracter == '|':
                self.addNodeOr()
            elif caracter == '*':
                self.getNodeCloseState()
        self.init, self.final = self.queue.pop()
        return self.graph
