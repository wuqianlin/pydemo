import collections
import logging
import re

# Token specification
NUM = r'(?P<NUM>\d+(\.\d*)?)'

_func = '[a-zA-Z_][\w]*'
_metric = '[a-zA-Z_:][\w:]*'
_tag = '[a-zA-Z_][\w]*'
_lp = '\('
_rp = '\)'
_tv = '[\w]*?'
_offset = '(\s+offset\s+\[\d\])?'
VAR = f'''(?P<VAR>{_metric}{{({_tag}=(?P<q3>['"]){_tv}(?P=q3)(,{_tag}=(?P<q4>['"]){_tv}(?P=q4))*|\s*)}}.{_func}{_lp}.*?{_rp})'''

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

master_pat = re.compile('|'.join([
    NUM, VAR, PLUS, MINUS, TIMES, DIVIDE, GTE, LTE, GT, LT, EQUAL, UNEQUAL, LPAREN, RPAREN, WS]), flags=re.A | re.X)

Token = collections.namedtuple('Token', ['type', 'value'])

logger = logging.getLogger('app.running.log')


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
        """
        Advance one token ahead
        """
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        """
        Test and consume the next token if it matched toktype
        """
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self, toktype):
        """
        Consume next toke if it matches toktype or raise SyntaxError
        """
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    def bool(self):
        """
        bool ::= expression {'=='|'!='|'>='|'<='|'>'|'<'}
        """
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
        """
        expression ::= term { ('+'|'-') term }
        """
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
        """
        term ::= factor { ('*'|'/') factor }
        """
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
        """
        factor ::= NUM | VAR | (expr)
        """
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


NUMBER_PATTERN = re.compile('\d+(\.\d*)?')
METRIC_PATTERN = re.compile(r'(?P<metric>[a-zA-Z_:][\w:]*){(?P<tags>.*?)}\.(?P<func>\w+)\((?P<para>[\w,]*)\)', re.ASCII)

expression_tree_builder = ExpressionTreeBuilder()


class AlarmSyntaxError(Exception):
    """
    告警表达式语法错误
    """


def var_replace(variable):
    if NUMBER_PATTERN.fullmatch(variable):
        return variable
    else:
        metric_expr = METRIC_PATTERN.fullmatch(variable)
        if metric_expr:
            _metric_expr = metric_expr.groupdict()
            metric = _metric_expr.get('metric')
            tags = _metric_expr.get('tags')
            func = _metric_expr.get('func')
            para = _metric_expr.get('para')
            return {
                'metric': metric,
                'tags': tags,
                'func': func,
                'para': para,
            }
        else:
            raise SyntaxError('Variable format is wrong!')


def encapsulate(parse_tree: tuple):
    sign, prefix, suffix = parse_tree
    if isinstance(prefix, str):
        prefix = var_replace(prefix)
    elif isinstance(prefix, tuple) and len(prefix) == 3:
        prefix = encapsulate(prefix)
    else:
        raise SyntaxError('Expression Tree Error')

    if isinstance(suffix, str):
        suffix = var_replace(suffix)
    elif isinstance(suffix, tuple) and len(suffix) == 3:
        suffix = encapsulate(suffix)
    else:
        raise SyntaxError('Expression Parse Tree Error')

    # final_expr = f"{prefix}{sign}{suffix}"
    final_expr = (sign, prefix, suffix,)
    return final_expr


def parse_alert_expr(expr: str):
    try:
        _expr_parse_tree = expression_tree_builder.parse(expr)
        _encapsulate = encapsulate(_expr_parse_tree)
    except SyntaxError as e:
        raise AlarmSyntaxError(e)
    return _encapsulate


if __name__ == "__main__":
    expr_list = [
        # '2 + 3',
        # '2 + 3 * 4',
        # '45 >= 2 + (3 + 4) * 5',
        # '2 + 3 + 4',
        # "fifteen_minutes{host='host_01',mode='2'}.avg(3600,86400)}>0.6",
        # "fifteen_minutes{host='host_01'}.avg(3600,86400)}>0.6",
        # "fifteen_minutes{host='host_01'}.avg(3600,86400)}>0.6",
        # "fifteen_minutes{}.avg(3600,86400)}>0.6",
        # "fifteen_minutes{   }.avg(3600,86400)}>0.6",
        # 'fifteen_minutes{}.avg(3600,86400)} - fifteen_minutes{}.sum(3600,86400)} > 0.7',
        # '1 - fifteen_minutes{}.avg(3600,86400) / fifteen_minutes{}.avg(3600,86400)}> 1',
        # 'fifteen_minutes{}.avg(3600,86400) + fifteen_minutes{}.avg(3600,86400) > 86400',
        # 'fifteen_minutes{}.avg(3600,86400)}>0.6',
        # 'fifteen_minutes{}.avg(3600,86400) - 89 + 0.7',
        # 'model_name{}.last()>=0',
        'CpuLoad::fifteen_minutes{}.last()>=0',
        'CpuLoad::one_minute{}.last()>=0.1'
    ]
    for s in expr_list:
        print(expression_tree_builder.parse(s))

    parsed_expr_list = [
        # ('+', '2', '3'),
        # ('+', '2', ('*', '3', '4')),
        # ('>=', '45', ('+', '2', ('*', ('+', '3', '4'), '5'))),
        # ('+', ('+', '2', '3'), '4'),
        # ('>', "fifteen_minutes{host:host_01,mode:2}.avg(3600,86400)", '0.6'),
        # ('>', "fifteen_minutes{hosthost_01}.avg(3600,86400)", '0.6'),
        # ('>', 'fifteen_minutes{}.avg(3600,86400)', '0.6'),
        # ('>', 'fifteen_minutes{   }.avg(3600,86400)', '0.6'),
        # ('>', ('-', 'fifteen_minutes{}.avg(3600,86400)', 'fifteen_minutes{}.sum(3600,86400)'), '0.7'),
        # ('>', ('-', '1', ('/', 'fifteen_minutes{}.avg(3600,86400)', 'fifteen_minutes{}.avg(3600,86400)')), '1'),
        # ('>', ('+', 'fifteen_minutes{}.avg(3600,86400)', 'fifteen_minutes{}.avg(3600,86400)'), '86400'),
        # ('>', 'fifteen_minutes{}.avg(3600,86400)', '0.6'),
        # ('+', ('-', 'fifteen_minutes{}.avg(3600,86400)', '89'), '0.7'),
        # ('>=', 'model_name{}.last(1)', '0'),
        ('>=', 'CpuLoad::fifteen_minutes{}.last()', '0'),
        ('>=', 'CpuLoad::one_minute{}.last()', '0.1')
    ]

    for first_parsed_expr in parsed_expr_list:
        _final_expr = encapsulate(first_parsed_expr)
        print(_final_expr)
