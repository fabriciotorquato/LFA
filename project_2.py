#!/usr/bin/python
# -*- coding: utf-8 -*-

from edge import Edge
from node import Node
from graph import Graph

node_name = 0

def converterPosFixa(expressao):
    posfixa = ''
    pilha = []

    for c in expressao:
        if (c >= 'A' and c <= 'Z'):
            posfixa += c
        if c == '+' or c == '.' or (c == '*'):
            pr = valor_prioridade(c)
            while len(pilha) > 0 and valor_prioridade(pilha[len(pilha)-1]) >= pr:
                posfixa += pilha.pop()
            pilha.append(c)
        if c == '[' or c == '{' or c == '(':
            pilha.append(c)
        if c == ']' or c == '}' or c == ')':
            x = pilha.pop()
            while x != '(' and x != '{' and x != '[':
                posfixa += x
                x = pilha.pop()
    while len(pilha) > 0:
        posfixa += pilha.pop()

    return posfixa


def verificarExpressao(expressao):
    pilha = []
    for c in expressao:
        if c == '[' or c == '{' or c == '(':
            pilha.append(c)
        elif c == ']' or c == '}' or c == ')':
            if len(pilha) == 0:
                return False
            abre = pilha.pop()
            if (c == ')' and abre != '(') or (c == ']' and abre != '[') or (c == '}' and abre != '{'):
                return False

    if len(pilha) > 0:
        return False
    return True


def valor_prioridade(c):
    if c == '[' or c == '{' or c == '(':
        return 1
    if c == '+':
        return 2
    if c == '.':
        return 3
    if c == '*':
        return 4
    return 0


if __name__ == "__main__":

    value = converterPosFixa('(A+B).C')
    print(value)
    graph = Graph()
    queue = []

    for caracter in value:
        if (caracter >= 'A' and caracter <= 'Z'):
            edge = Edge(None,caracter)

            second_node = Node(node_name)
            node_name+=1
            edge.node = second_node
            fisrt_node = Node(node_name)
            fisrt_node.edges.append(edge)
            node_name+=1

            queue.append((fisrt_node, second_node))

            graph.list_node.append(fisrt_node)
            graph.list_node.append(second_node)
            graph.list_edge.append(edge)

        elif caracter == '.':

            first_node_1, second_node_1 = queue.pop()
            first_node_0, second_node_0 = queue.pop()

            edge = Edge(first_node_1, '&')
            graph.list_edge.append(edge)
            second_node_0.edges.append(edge)

            edge = Edge(first_node_0, '&')
            graph.list_edge.append(edge)

            init_node = Node(node_name)
            init_node.edges.append(edge)
            node_name+=1
            graph.list_node.append(init_node)

            final_node = Node(node_name)
            node_name+=1
            graph.list_node.append(final_node)
            edge = Edge(final_node, '&',)
            graph.list_edge.append(edge)
            second_node_1.edges.append(edge)

            queue.append((init_node, final_node))

        elif caracter == '+':
            first_node_1, second_node_1 = queue.pop()
            first_node_0, second_node_0 = queue.pop()


            init_node = Node(node_name)
            node_name+=1
            graph.list_node.append(init_node)

            edge_node_1 = Edge(first_node_1, '&',)
            graph.list_edge.append(edge)
            edge_node_0 = Edge(first_node_0, '&',)
            graph.list_edge.append(edge)

            init_node.edges.append(edge_node_1)
            init_node.edges.append(edge_node_0)

            final_node = Node(node_name)
            node_name+=1
            graph.list_node.append(final_node)

            edge_node_1 = Edge(final_node, '&',)
            graph.list_edge.append(edge)
            edge_node_0 = Edge(final_node, '&',)
            graph.list_edge.append(edge)

            second_node_1.edges.append(edge_node_1)
            second_node_0.edges.append(edge_node_0)

            queue.append((init_node, final_node))




    init,final = queue.pop()
    print("Inicial ",init.name)
    print("Final ",final.name)


    graph.show()