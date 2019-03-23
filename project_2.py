#!/usr/bin/python
# -*- coding: utf-8 -*-


from postfixNotation import PostfixNotation
from finiteStateMachine import FiniteStateMachine

if __name__ == "__main__":
    postfixNotation = PostfixNotation('(A.B).(C|A)')
    value = postfixNotation.expression_postfix
    print(value)
    finiteStateMachine = FiniteStateMachine(postfixNotation)
    finiteStateMachine.getNFA().show()
