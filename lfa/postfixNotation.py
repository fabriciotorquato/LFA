
class PostfixNotation():
    def __init__(self, expression):
        self.expression = self.convertMinOneValue(expression)
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
                char_open = self.getOpenChar(c)
                while x != char_open:
                    posfixa += x
                    x = pilha.pop()
        while pilha:
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

        if pilha:
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

    def getCloseChar(self, char_open):
        if char_open == '(':
            return ')'
        elif char_open == '{':
            return '}'
        elif char_open == '[':
            return ']'
        return ''

    def getOpenChar(self, char_close):
        if char_close == ')':
            return '('
        elif char_close == '}':
            return '{'
        elif char_close == ']':
            return '['
        return ''

    def convertMinOneValue(self, olf_expression):
        queue = []
        for c in olf_expression:
            if c == '+':
                x = queue.pop()

                if x != ')' and x != '}' and x != ']':
                    queue.append(x)
                    queue.append('.')
                    queue.append(x)
                    queue.append('*')
                else:
                    queue_aux = []
                    char_close = self.getOpenChar(x)

                    while x != char_close:
                        queue_aux.append(x)
                        x = queue.pop()

                    queue_aux.append(x)

                    queue_aux.reverse()

                    for x in queue_aux:
                        queue.append(x)

                    queue.append('.')

                    for x in queue_aux:
                        queue.append(x)

                    queue.append('*')
            else:
                queue.append(c)
        return ''.join(queue)
