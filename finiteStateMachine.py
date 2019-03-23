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
        first_node_1, second_node_1 = self.queue.pop()
        first_node_0, second_node_0 = self.queue.pop()

        edge = Edge(first_node_1, '&')
        self.graph.list_edge.append(edge)
        second_node_0.edges.append(edge)

        edge = Edge(first_node_0, '&')
        self.graph.list_edge.append(edge)

        init_node = Node(self.graph.getNextName())
        init_node.edges.append(edge)

        self.graph.list_node.append(init_node)

        final_node = Node(self.graph.getNextName())

        self.graph.list_node.append(final_node)
        edge = Edge(final_node, '&',)
        self.graph.list_edge.append(edge)
        second_node_1.edges.append(edge)

        self.queue.append((init_node, final_node))

    def addNodeOr(self):
        first_node_1, second_node_1 = self.queue.pop()
        first_node_0, second_node_0 = self.queue.pop()

        init_node = Node(self.graph.getNextName())

        self.graph.list_node.append(init_node)

        edge_node_1 = Edge(first_node_1, '&',)
        self.graph.list_edge.append(edge_node_1)
        edge_node_0 = Edge(first_node_0, '&',)
        self.graph.list_edge.append(edge_node_0)

        init_node.edges.append(edge_node_1)
        init_node.edges.append(edge_node_0)

        final_node = Node(self.graph.getNextName())

        self.graph.list_node.append(final_node)

        edge_node_1 = Edge(final_node, '&',)
        self.graph.list_edge.append(edge_node_1)
        edge_node_0 = Edge(final_node, '&',)
        self.graph.list_edge.append(edge_node_0)

        second_node_1.edges.append(edge_node_1)
        second_node_0.edges.append(edge_node_0)

        self.queue.append((init_node, final_node))

    def getNodeCloseState(self):
        pass

    def addNodeState(self, caracter):
        edge = Edge(None, caracter)

        fisrt_node = Node(self.graph.getNextName())
        second_node = Node(self.graph.getNextName())
        edge.node = second_node

        fisrt_node.edges.append(edge)

        self.queue.append((fisrt_node, second_node))

        self.graph.list_node.append(fisrt_node)
        self.graph.list_node.append(second_node)
        self.graph.list_edge.append(edge)

    def getNFA(self):
        for caracter in self.postfixNotation.expression_postfix:
            if (caracter >= 'A' and caracter <= 'Z'):
                self.addNodeState(caracter)
            elif caracter == '.':
                self.addNodeAnd()
            elif caracter == '|':
                self.addNodeOr()
        self.init, self.final = self.queue.pop()
        return self.graph
