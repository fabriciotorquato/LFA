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
        self.solutions = {}
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
        
        graphNFA = self.getNFA()
        graphDFA = Graph()


        initial_node = self.init
        solution_index = 0
        solutions_queaue = []

        #A chave é a lista com os Qs ... Preciso de alguma maneira de deixar eles em ordem, pois ai comparo as chaves, ai não adiciona outro novo valor
        self.solutions['S'+solution_index] = self.getClosure(initial_node) 
        solutions_queaue.append('S'+solution_index)
        solution_index = solution_index + 1    
        
        while len(solutions_queaue) > 0:
            actual_solution = solutions_queaue.pop(0)
            for caracter in self.alphabet:
              new_solution =  self.dfaEdge(actual_solution, caracter)
              #Verifica se a solution ja esta ans solution
              #caso nao esteja adiciona a nova Solution
              #Talvez precisamos de uma lista para guardar o valor das solutions indo para onde (s0, x s1) opa, esse é o grafo, atualizar o novo grafo










    def getClosure(self, initial_node):
        visited_nodes = []
        queaue_nodes = []
        visited_nodes.append(initial_node)
        queaue_nodes.append(initial_node)

        
        while len(queaue_nodes) > 0:
            node = queaue_nodes.pop(0)
            for ed in node.edges:
                if ed.name == '&':
                    visited_nodes.append(ed.node)
                    queaue_nodes.append(ed.node)

        return list(set(visited_nodes))

    def dfaEdge(self, solution, value):
        list_nodes = self.solutions[solution]

        visited_nodes = []
        queaue_nodes = list_nodes.copy()

        while len(queaue_nodes) > 0:
            node = queaue_nodes.pop(0)
            for ed in node.edges:
                if ed.name == '&':
                    visited_nodes.append(ed.node)
                    queaue_nodes.append(ed.node)
                if  ed.name == value:
                    visited_nodes.append(ed.node)

        return list(set(visited_nodes))
        






























































        










