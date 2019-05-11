#!/usr/bin/python
# -*- coding: utf-8 -*-


from lfa.postfixNotation import PostfixNotation
from lfa.finiteStateMachine import FiniteStateMachine

if __name__ == "__main__":
    postfixNotation = PostfixNotation('(A|B).(A|B)')
    print("Expressão Regular")
    print(postfixNotation.expression)
    print("Expressão Regular em Posfixa")
    print(postfixNotation.expression_postfix)
    finiteStateMachine = FiniteStateMachine(postfixNotation)
    finiteStateMachine.getDFAMini().show()