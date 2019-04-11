#!/usr/bin/python
# -*- coding: utf-8 -*-


from postfixNotation import PostfixNotation
from finiteStateMachine import FiniteStateMachine

if __name__ == "__main__":
    postfixNotation = PostfixNotation('(A|B).C')
    print("Expressão Regular")
    print(postfixNotation.expression)
    print("Expressão Regular em Posfixa")
    print(postfixNotation.expression_postfix)
    finiteStateMachine = FiniteStateMachine(postfixNotation)
    finiteStateMachine.getDFA().show()
