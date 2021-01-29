import re


def sub_parse():
    log_str = "{8902}/{8901}<0.7"
    value = { 8901:'123', 8902:'134' }
    for k, v in value.items():
        v = str(v)
        k = str(k)
        log_str = re.sub(f"\{{{k}\}}", v, log_str)

    print(log_str)
    print(eval(log_str))


def expr_parse(expr):
    expr_pattern = re.compile(r'{(?P<field_name>\w+)\.(?P<func_name>\w+)\((?P<parameter>[\w,]+)\)}', re.ASCII)
    match = expr_pattern.match(expr)
    if match:
        print(match.groupdict())
    else:
        print("nothing")

replace_pattern = re.compile(r'{(?P<field_name>\w+)\.(?P<func_name>\w+)\((?P<parameter>[\w,]+)\)}', re.ASCII)
number = re.compile('\d+(\.\d*)?')

def var_replace(variable):
    if number.fullmatch(variable):
        return variable
    else:
        match = replace_pattern.match(variable)
        if match:
            print(match.groupdict())
            return 'replace'
        else:
            raise SyntaxError('Variable format is wrong!')


def parse_avg(expression):
    sign, prefix, suffix = expression
    if isinstance(prefix, str):
        prefix = var_replace(prefix)
    elif isinstance(prefix, tuple) and len(prefix) == 3:
        prefix = parse_avg(prefix)
    else:
        raise SyntaxError('Expression Tree Error')

    if isinstance(suffix, str):
        suffix = var_replace(suffix)
    elif isinstance(suffix, tuple) and len(suffix) == 3:
        suffix = parse_avg(suffix)
    else:
        raise SyntaxError('Expression Tree Error')

    final_expr = f"{prefix} {sign} {suffix}"
    return final_expr


if "__main__" == __name__:
    expr1 = '{fifteen_minutes.avg(3600,86400)}>0.6'
    expr2 = '{fifteen_minutes.avg(3600,86400)} - {fifteen_minutes.sum(3600,86400)} > 0.7'
    expr3 = '{fifteen_minutes.avg(3600,86400)} / {fifteen_minutes.avg(3600,86400)} > 1'
    expr4 = '{fifteen_minutes.avg(3600,86400)}+{fifteen_minutes.avg(3600,86400)}>86400'
    expr5 = '{fifteen_minutes.avg(3600,,,86400)}>0.6'

    expression = ('>', ('-', '1', ('/', '{fifteen_minutes.avg(3600,0)}', '{fifteen_minutes.avg(3600,86400)}')), '1')
    res = parse_avg(expression)
    print(res)

    var1 = '{fifteen_minutes.avg(3600,86400)}'
    var2 = '{fifteen_minutes.avg(3600,)}'
    var3 = '{fifteen_minutes.avg(3600)}'
    var_replace(var1)
    var_replace(var2)
    var_replace(var3)

