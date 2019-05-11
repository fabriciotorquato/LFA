#!/usr/bin/python
# -*- coding: utf-8 -*-

from .edge import Edge
from .dfaNode import DFANode
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

        closure = DFANode(graphDFA.getNextState())
        closure.nodes = self._getClosure(initial_node)
        closure.convertStringSolution()
        graphDFA.addNodes([closure])

        solution_nodes[closure.name] = closure.nodes_name

        queue = [closure]
        closure.is_initial_node = True
        graphDFA.node_init = closure

        while queue:
            actual_DFAnode = queue.pop()

            for caracter in self.alphabet:

                solution = self._getDFAnode(actual_DFAnode, caracter)
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
                        state = DFANode(graphDFA.getNextState())
                        state.nodes = solution
                        state.convertStringSolution()

                        graphDFA.addNodes([state])

                        solution_nodes[state.name] = state.nodes_name
                        queue.append(state)

                        edge = Edge(None, caracter)
                        edge.node = state
                        actual_DFAnode.edges.append(edge)
                        graphDFA.addEdges([edge])

                    else:

                        node_name = self._findNodeName(
                            solution_nodes, string_solution)

                        edge = Edge(None, caracter)
                        edge.node = graphDFA.findNode(node_name)
                        actual_DFAnode.edges.append(edge)
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

    def _getDFAnode(self, dfaNode, value):
        name_visited_nodes = []
        visited_nodes = []
        queue_nodes = dfaNode.nodes.copy()

        while queue_nodes:
            node = queue_nodes.pop()
            for ed in node.edges:
                if ed.name == value and ed.node.name not in name_visited_nodes:
                    name_visited_nodes.append(ed.node.name)
                    visited_nodes.append(ed.node)
                    queue_nodes.append(ed.node)

        return visited_nodes

    def getDFAMini(self):
        graphDFA = self.getDFA()

        graphDFAMini = self._remove_states_unreachable(graphDFA)
        graphDFAMini = self._validaded_DFA(graphDFAMini)
        hash_table = {}

        # Marcar estados trivialmente não-equivalentes {estado final, estado não-final}
        for node_A in graphDFAMini.list_node:
            for node_B in graphDFAMini.list_node:
                tupla_name = [node_A.name, node_B.name]
                tupla_name.sort()
                tupla_name = tuple(tupla_name)
                if node_A.is_final_node == node_B.is_final_node and node_A.name != node_B.name:
                    if tupla_name not in hash_table:
                        hash_table[tupla_name] = 0
                else:
                    if tupla_name not in hash_table:
                        hash_table[tupla_name] = 1

        list_possibled = {}

        for key, value in hash_table.items():
            if value == 0:
                nodes_equivales_key1 = []
                nodes_equivales_key2 = []

                for caracter in self.alphabet:
                    nodes_equivales_key1.append(
                        graphDFAMini.findEdgeCaracter(key[0], caracter).name)
                    nodes_equivales_key2.append(
                        graphDFAMini.findEdgeCaracter(key[1], caracter).name)
                
                nodes_equivales_key1.sort()
                nodes_equivales_key2.sort()

                nodes_equivales_key1 = tuple(nodes_equivales_key1)
                nodes_equivales_key2 = tuple(nodes_equivales_key2)

                if hash_table[nodes_equivales_key1] == 1 or hash_table[nodes_equivales_key2] == 1:

                    hash_table[key] = 1
                    hash_table, list_possibled = self._verific_possibled_key(
                        hash_table, list_possibled, key)
                else:
                    if key not in list_possibled:
                        list_possibled[key] = [
                            nodes_equivales_key1, nodes_equivales_key2]
                    else:
                        list_possibled[key].append(nodes_equivales_key1)
                        list_possibled[key].append(nodes_equivales_key2)

        print(hash_table)

        for key, value in hash_table.items():
            if value == 0:
                edges_in_1, edges_out_1, is_final_node, is_initial_node_1 = graphDFAMini.removeNode(
                    key[0])
                edges_in_2, edges_out_2, is_final_node, is_initial_node_2 = graphDFAMini.removeNode(
                    key[0])

                union_node = DFANode(
                    graphDFAMini.getNextState(), is_final_node=is_final_node, is_initial_node=(is_initial_node_1 or is_initial_node_2) )
                graphDFAMini.addNodes([union_node])

                if union_node.is_initial_node:
                    print("SSSSSSSSSSsss", union_node.name)
                    graphDFAMini.node_init = union_node

                for edge in edges_in_1:
                    edge.node = union_node

                for edge in edges_in_2:
                    edge.node = union_node

                union_node.edges = edges_out_1
                union_node.edges.extend(edges_out_2)

        graphDFAMini.removeJoker()

        return graphDFAMini

    def _verific_possibled_key(self, hash_table, list_possibled, key):
        queue = [key]
        while len(queue):
            current = queue.pop()
            if current in list_possibled:
                for k in list_possibled[current].items():
                    hash_table[k] = 1
                    queue.append(k)
                list_possibled.remove(current)

        return hash_table, list_possibled

    def _validaded_DFA(self, graph):

        node_joker = DFANode(graph.getjokerState(), is_final_node=True)
        have_inlcude_joker = False

        for node in graph.list_node:
            for caracter in self.alphabet:
                is_caracter_include = False
                for edge in node.edges:
                    if edge.name == caracter:
                        is_caracter_include = True
                if not is_caracter_include:
                    if not have_inlcude_joker:
                        graph.addNodes([node_joker])
                        have_inlcude_joker = True
                    edge = Edge(node_joker, caracter)
                    graph.addEdges([edge])
                    node.edges.append(edge)
        return graph

    def _create_nodeDFA_joker(self, graph):
        dfaNode = DFANode(graph.getjokerState())
        edges = []
        for caracter in self.alphabet:
            edge = Edge(dfaNode, caracter)
            edges.append(edge)
        return dfaNode, edges

    def _remove_states_unreachable(self, graph):
        graph_reachable = Graph()
        graph_reachable.node_name = graph.node_name
        graph_reachable.state_name = graph.state_name

        initial_nodes = graph.node_init
        graph_reachable.node_init = initial_nodes
        graph_reachable.node_init.is_initial_node = True
        queue = [initial_nodes]

        memory_nodes_name = [initial_nodes.name]

        while len(queue):
            current_node = queue.pop()
            graph_reachable.addNodes([current_node])
            for edge in current_node.edges:
                if edge.node.name not in memory_nodes_name:
                    memory_nodes_name.append(edge.node.name)
                    queue.append(edge.node)

        for node in graph.node_finals:
            for new_nodes in graph_reachable.list_node:
                if new_nodes.name == node:
                    new_nodes.is_final_node = True
                    graph_reachable.node_finals.append(new_nodes.name)

        return graph_reachable
