import re
import sys
import collections


# Token specification
NUM = r'(?P<NUM>\d+(\.\d*)?)'
VAR = r'(?P<VAR>{[\w,\(\).]+})'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'

EQUAL = r'(?P<EQUAL>==)'
UNEQUAL = r'(?P<UNEQUAL>!=)'
GTE = r'(?P<GTE>>=)'
LTE = r'(?P<LTE><=)'
GT = r'(?P<GT>>)'
LT = r'(?P<LT><)'

# ,

master_pat = re.compile('|'.join([NUM, VAR, PLUS, MINUS, TIMES, DIVIDE, GTE, LTE, GT, LT, EQUAL, UNEQUAL, LPAREN, RPAREN, WS]))

#Tokenizer
Token = collections.namedtuple('Token', ['type', 'value'])

def generate_tokens(text):
    scanner = master_pat.finditer(text)
    for m in scanner:
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok


class ExpressionTreeBuilder:
    tokens = None
    tok = None
    nexttok = None

    def parse(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None
        self.nexttok = None
        self._advance()
        return self.bool()

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

    def bool(self):
        """bool ::= expression {'=='|'!='|'>='|'<='|'>'|'<'}"""

        boolval = self.expr()
        while self._accept('EQUAL') or self._accept('UNEQUAL') or self._accept('GTE') or \
                self._accept('LTE') or self._accept('GT') or self._accept('LT'):
            op = self.tok.type
            right = self.expr()
            if op == 'EQUAL':
                boolval = ('==', boolval, right)
            elif op == 'UNEQUAL':
                boolval = ('!=', boolval, right)
            elif op == 'GTE':
                boolval = ('>=', boolval, right)
            elif op == 'LTE':
                boolval = ('<=', boolval, right)
            elif op == 'GT':
                boolval = ('>', boolval, right)
            elif op == 'LT':
                boolval = ('<', boolval, right)
        return boolval

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
        """factor ::= NUM | VAR | (expr)"""

        if self._accept('NUM'):
            return self.tok.value
        elif self._accept('VAR'):
            return self.tok.value
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')


expr0 = '2 + 3'
expr1 = '2 + 3 * 4'
expr2 = '45 >= 2 + (3 + 4) * 5'
expr3 = '2 + 3 + 4'
expr4 = '{fifteen_minutes.avg(3600,86400)}>0.6'
expr5 = '{fifteen_minutes.avg(3600,86400)} - {fifteen_minutes.sum(3600,86400)} > 0.7'
expr6 = '1 - {fifteen_minutes.avg(3600,86400)} / {fifteen_minutes.avg(3600,86400)}> 1'
expr7 = '{fifteen_minutes.avg(3600,86400)}+{fifteen_minutes.avg(3600,86400)}>86400'
expr8 = '{fifteen_minutes.avg(3600,,,86400)}>0.6'
expr9 = '{fifteen_minutes.avg(3600,86400)} - 89 + 0.7'

# for x in generate_tokens(expr4):
#     print(x)

et = ExpressionTreeBuilder()
mod = sys.modules[__name__]
for index in range(10):
    print( et.parse(getattr(mod, f'expr{index}')) )


# print( et.parse(expr6))





