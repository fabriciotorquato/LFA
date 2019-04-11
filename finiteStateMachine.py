#!/usr/bin/python
# -*- coding: utf-8 -*-

from edge import Edge
from DFAedge import DFAedge
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

    def addDFAedgeNode(self, fisrt_node, caracter, second_node, graph):
        edge = Edge(None, caracter)

        edge.node = second_node
        if graph.addEdges([edge]):
            fisrt_node.edges.append(edge)

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
        self.init, self.final = self.queue.pop()
        self.alphabet = list(set(self.alphabet))
        return self.graph

    def getDFA(self):

        _ = self.getNFA()
        graphDFA = Graph()

        initial_node = self.init
        queue = []

        closure = self.getClosure(initial_node)

        closure_node = DFAedge(graphDFA.getNextState())
        closure_node.nodes = closure
        closure_node.nodes_name = closure_node.getStringSolution()
        graphDFA.addNodes([closure_node])

        self.list_solutions_nodes[closure_node.name] = closure_node.nodes_name

        queue.append(closure_node)

        while len(queue) > 0:
            actual_DFAedge = queue.pop()
            new_solution = []
            for caracter in self.alphabet:
                new_solution = self.searchDFAedge(actual_DFAedge, caracter)
                new_solution_visited = []

                for node in new_solution:
                    new_solution_visited.append(node.name)
                
                if len(new_solution) != 0:
                    #Teve algum no depois                   Aplicar o closure para cada Node e juntar tudo virando o novo node_name
                    solutions = []
                    for node in new_solution:
                        nodes_e = self.getClosure(node)
                        for node_aux in nodes_e:
                            if node_aux.name not in new_solution_visited:
                                new_solution_visited.append(node_aux.name)
                                solutions.append(node_aux)  

                    for node in solutions:
                        new_solution.append(node) 

                    new_solution.sort(key=lambda x: x.name)

                    string_solution = graphDFA.getStringSolution(new_solution)
                        
                    if string_solution not in self.list_solutions_nodes.values():
                        new_state = DFAedge(graphDFA.getNextState())
                        new_state.nodes = new_solution
                        new_state.nodes_name = new_state.getStringSolution()

                        graphDFA.addNodes([new_state])

                        self.list_solutions_nodes[new_state.name] = new_state.nodes_name
                        queue.append(new_state)

                        edge = Edge(None, caracter)
                        edge.node = new_state
                        actual_DFAedge.edges.append(edge)
                        
                        graphDFA.addEdges([edge])
                    else:
                        node_name = ''
                        for name, node_name in self.list_solutions_nodes.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
                            if string_solution == node_name:
                                node_name = name
                                break;

                        edge = Edge(None, caracter)
                        edge.node = graphDFA.findNode(node_name)
                        actual_DFAedge.edges.append(edge)
                        graphDFA.addEdges([edge])

        
        #graphDFA.clearNodes()
        
        return graphDFA

    def getClosure(self, initial_node):
        visited_nodes = []
        name_visited_nodes = []
        queue_nodes = []
        name_visited_nodes.append(initial_node.name)

        visited_nodes.append(initial_node)
        queue_nodes.append(initial_node)

        while len(queue_nodes) > 0:
            node = queue_nodes.pop(0)
            for ed in node.edges:
                if ed.name == "&":
                    if ed.node.name not in name_visited_nodes:
                        name_visited_nodes.append(ed.node.name)
                        visited_nodes.append(ed.node)
                        queue_nodes.append(ed.node)


        visited_nodes.sort(key=lambda x: x.name)
        return visited_nodes

    def searchDFAedge(self, dfaEdge, value):
        name_visited_nodes = []
        visited_nodes = []
        queue_nodes = []
        for node in dfaEdge.nodes:
            queue_nodes.append(node)

        while len(queue_nodes) > 0:
            node = queue_nodes.pop(0)
            for ed in node.edges:
                if ed.name == value:
                    if ed.node.name not in name_visited_nodes:
                        name_visited_nodes.append(ed.node.name)
                        visited_nodes.append(ed.node)
                        queue_nodes.append(ed.node)
                    
        visited_nodes.sort(key=lambda x: x.name)
        return visited_nodes
