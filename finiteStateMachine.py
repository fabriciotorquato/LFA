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
        self.list_solutions_nodes = {}
        self.alphabet = []

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

    def addDFAedgeNode(self, fisrt_node, caracter, node_2, graph):
        edge = Edge(None, caracter)

        second_node = Node(node_2)

        edge.node = second_node
        fisrt_node.edges.append(edge)

        graph.addNodes([fisrt_node, second_node])
        graph.addEdges([edge])
        return graph

    def getNFA(self):
        for caracter in self.postfixNotation.expression_postfix:
            if (caracter >= 'A' and caracter <= 'Z' or caracter >= 'a' and caracter <= 'z'):
                self.addNodeState(caracter)
                self.alphabet.append(caracter)
            elif caracter == '.':
                self.addNodeAnd()
            elif caracter == '|':
                self.addNodeOr()
            elif caracter == '*':
                self.getNodeCloseState()
        self.final, self.init = self.queue.pop()
        self.alphabet = list(set(self.alphabet))
        return self.graph

    def getDFA(self):

        _ = self.getNFA()
        graphDFA = Graph()

        initial_node = self.init
        solutions_queaue = []

        closure = self.getClosure(initial_node)
        string_solution = graphDFA.getStringSolution(
            closure)

        self.list_solutions_nodes[graphDFA.getCurrentState()] = string_solution

        closure_node = Node(graphDFA.getCurrentState())
        solutions_queaue.append(closure_node)
        graphDFA.addNodes([closure_node])

        while len(solutions_queaue) > 0:
            actual_solution = solutions_queaue.pop(0)
            new_solution = []
            for caracter in self.alphabet:

                new_solution = self.dfaEdge(actual_solution, caracter)
                if len(new_solution) != 0:
                    string_solution = graphDFA.getStringSolution(
                        new_solution)
                    print(string_solution)

                    if string_solution not in self.list_solutions_nodes:

                        self.list_solutions_nodes[graphDFA.getCurrentState(
                        )] = string_solution

                        current_node = Node(graphDFA.getCurrentState())
                        solutions_queaue.append(current_node)
                        graphDFA.addNodes([current_node])

                        graphDFA = self.addDFAedgeNode(
                            actual_solution, caracter, current_node, graphDFA)
                    else:
                        node_name = self.list_solutions_nodes.keys(
                        )[self.list_solutions_nodes.values().index(string_solution)]
                        graphDFA = self.addDFAedgeNode(
                            actual_solution, caracter, graphDFA.findNode(node_name), graphDFA)

        return graphDFA

    def getClosure(self, initial_node):
        visited_nodes = []
        queaue_nodes = []
        visited_nodes.append(initial_node)
        queaue_nodes.append(initial_node)

        while len(queaue_nodes) > 0:
            node = queaue_nodes.pop(0)
            for ed in node.edges:
                if ed.name == '&' and any(node.name == ed.name for node in visited_nodes):
                    visited_nodes.append(ed.node)
                    queaue_nodes.append(ed.node)

        visited_nodes.sort(key=lambda x: x.name)
        return visited_nodes

    def dfaEdge(self, solution, value):

        visited_nodes = []
        queaue_nodes = []
        queaue_nodes.append(solution)

        while len(queaue_nodes) > 0:
            node = queaue_nodes.pop(0)
            print(len(node)
            for ed in node.edges:
                print(ed.name)
                if (ed.name == '&' or ed.name == value) and any(n.name == ed.name for n in visited_nodes):
                    visited_nodes.append(ed.node)
                    queaue_nodes.append(ed.node)

        visited_nodes.sort(key=lambda x: x.name)
        return visited_nodes
