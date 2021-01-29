import re
import collections


# Token specification
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS]))

#Tokenizer
Token = collections.namedtuple('Token', ['type', 'value'])

def generate_tokens(text):
    scanner = master_pat.finditer(text)
    for m in scanner:
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok

#parse
class ExpressionEvaluator:
    tokens = None
    tok = None
    nexttok = None


    def parse(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None
        self.nexttok = None
        self._advance()
        return self.expr()

    def _advance(self):
        """Advance one token ahead"""
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        """Test and consume the next token if it matched toktype"""
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self, toktype):
        """Consume next toke if it matches toktype or raise SyntaxError"""
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    # Grammar rules follow
    def expr(self):
        """expression ::= term { ('+'|'-') term }*"""

        exprval = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.tok.type
            right = self.term()
            if op == 'PLUS':
                exprval += right
            elif op == 'MINUS':
                exprval -= right
        return exprval

    def term(self):
        """term ::= factor { ('*'|'/') factor }*"""

        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            if op == 'TIMES':
                termval *= right
            elif op == 'DIVIDE':
                termval /= right
        return termval

    def factor(self):
        """factor ::= NUM | ( expr )"""

        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')



e = ExpressionEvaluator()
print( e.parse('2') )
print( e.parse('2 + 3') )
print( e.parse('2 + 3 * 4') )
print( e.parse('2 + (3 + 4) * 5') )
# print( e.parse('2 + (3 + * 4') )


class ExpressionTreeBuilder(ExpressionEvaluator):
    def expr(self):
        """expression ::= term { ('+'|'-') term }"""

        exprval = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.tok.type
            right = self.term()
            if op == 'PLUS':
                exprval = ('+', exprval, right)
            elif op == 'MINUS':
                exprval = ('-', exprval, right)
        return exprval

    def term(self):
        """term ::= factor { ('*'|'/') factor }"""

        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            if op == 'TIMES':
                termval = ('*', termval, right)
            if op == 'DIVIDE':
                termval = ('/', termval, right)
        return termval

    def factor(self):
        """factor ::= NUM | (expr)"""

        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')


et = ExpressionTreeBuilder()
print( et.parse('2 + 3') )
print( et.parse('2 + 3 * 4') )
print( et.parse('2 + (3 + 4) * 5') )
print( et.parse('2 + 3 + 4') )
print( et.parse('2 + 3') )
