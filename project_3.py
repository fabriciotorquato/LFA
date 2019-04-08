#!/usr/bin/python
# -*- coding: utf-8 -*-


from postfixNotation import PostfixNotation
from finiteStateMachine import FiniteStateMachine

if __name__ == "__main__":
    postfixNotation = PostfixNotation('C.A.B')
    print(postfixNotation.expression)
    print(postfixNotation.expression_postfix)
    finiteStateMachine = FiniteStateMachine(postfixNotation)
    finiteStateMachine.getDFA().show()
