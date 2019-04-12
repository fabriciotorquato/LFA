#!/usr/bin/python
# -*- coding: utf-8 -*-

from .edge import Edge
from .dfaEdge import DFAEdge
from .node import Node
from .graph import Graph
from .utils import getStringSolution


class FiniteStateMachine():
    def __init__(self, postfixNotation):
        self.postfixNotation = postfixNotation
        self.graph = Graph()
        self.queue = []
        self.alphabet = set()

    def _addNodeAnd(self):
        first_node_1, second_node_1 = self.queue.pop()
        first_node_0, second_node_0 = self.queue.pop()

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

    def _addNodeOr(self):
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

    def _getNodeCloseState(self):
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

    def _addNodeState(self, caracter):
        edge = Edge(None, caracter)

        fisrt_node = Node(self.graph.getNextName())
        second_node = Node(self.graph.getNextName())

        edge.node = second_node
        fisrt_node.edges.append(edge)

        self.graph.addNodes([fisrt_node, second_node])
        self.graph.addEdges([edge])
        self.queue.append((fisrt_node, second_node))

    def getNFA(self):
        self.alphabet = set()

        for caracter in self.postfixNotation.expression_postfix:
            if caracter >= 'A' and caracter <= 'Z' or caracter >= 'a' and caracter <= 'z':
                self._addNodeState(caracter)
                self.alphabet.add(caracter)
            elif caracter == '.':
                self._addNodeAnd()
            elif caracter == '|':
                self._addNodeOr()
            elif caracter == '*':
                self._getNodeCloseState()

        self.graph.node_init, node_final = self.queue.pop()
        self.graph.node_finals = [node_final.name]
        return self.graph

    def _findNodeName(self, solution_nodes, string_solution):
        for name, node_name in solution_nodes.items():
            if string_solution == node_name:
                return name
        return ''

    def getDFA(self):

        graphNFA = self.getNFA()
        graphDFA = Graph()
        solution_nodes = dict()

        initial_node = graphNFA.node_init
        final_node = graphNFA.node_finals[0]

        closure = DFAEdge(graphDFA.getNextState())
        closure.nodes = self._getClosure(initial_node)
        closure.convertStringSolution()
        graphDFA.addNodes([closure])

        solution_nodes[closure.name] = closure.nodes_name

        queue = [closure]
        graphDFA.node_init = closure

        while queue:
            actual_DFAedge = queue.pop()

            for caracter in self.alphabet:

                solution = self._getDFAedge(actual_DFAedge, caracter)
                solution_visited = [node.name for node in solution]

                if solution:
                    solutions = []
                    for node in solution:
                        nodes_e = self._getClosure(node)
                        for node_aux in nodes_e:
                            if node_aux.name not in solution_visited:
                                solution_visited.append(node_aux.name)
                                solutions.append(node_aux)

                    [solution.append(node) for node in solutions]
                    string_solution = getStringSolution(solution)

                    if string_solution not in solution_nodes.values():
                        state = DFAEdge(graphDFA.getNextState())
                        state.nodes = solution
                        state.convertStringSolution()

                        graphDFA.addNodes([state])

                        solution_nodes[state.name] = state.nodes_name
                        queue.append(state)

                        edge = Edge(None, caracter)
                        edge.node = state
                        actual_DFAedge.edges.append(edge)
                        graphDFA.addEdges([edge])

                    else:

                        node_name = self._findNodeName(
                            solution_nodes, string_solution)

                        edge = Edge(None, caracter)
                        edge.node = graphDFA.findNode(node_name)
                        actual_DFAedge.edges.append(edge)
                        graphDFA.addEdges([edge])

        for name, node_name in solution_nodes.items():
            if str(final_node) in node_name.split('|'):
                graphDFA.node_finals.append(name)

        return graphDFA

    def _getClosure(self, initial_node):
        visited_nodes = [initial_node]
        name_visited_nodes = [initial_node.name]
        queue_nodes = [initial_node]

        while queue_nodes:
            node = queue_nodes.pop()
            for ed in node.edges:
                if ed.name == "&" and ed.node.name not in name_visited_nodes:
                    name_visited_nodes.append(ed.node.name)
                    visited_nodes.append(ed.node)
                    queue_nodes.append(ed.node)

        return visited_nodes

    def _getDFAedge(self, dfaEdge, value):
        name_visited_nodes = []
        visited_nodes = []
        queue_nodes = dfaEdge.nodes.copy()

        while queue_nodes:
            node = queue_nodes.pop()
            for ed in node.edges:
                if ed.name == value and ed.node.name not in name_visited_nodes:
                    name_visited_nodes.append(ed.node.name)
                    visited_nodes.append(ed.node)
                    queue_nodes.append(ed.node)

        return visited_nodes
