
class PostfixNotation():
    def __init__(self, expression):
        self.expression = expression
        self.expression_postfix = self.converterPosFixa()

    def converterPosFixa(self):
        expressao = self.expression
        posfixa = ''
        pilha = []
        for c in expressao:
            if (c >= 'A' and c <= 'Z'):
                posfixa += c
            if c == '|' or c == '.' or (c == '*'):
                pr = self.valor_prioridade(c)
                while len(pilha) > 0 and self.valor_prioridade(pilha[len(pilha)-1]) >= pr:
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

    def verificarExpressao(self):
        expressao = self.expression
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

    def valor_prioridade(self, c):
        if c == '[' or c == '{' or c == '(':
            return 1
        if c == '|':
            return 2
        if c == '.':
            return 3
        if c == '*':
            return 4
        return 0
