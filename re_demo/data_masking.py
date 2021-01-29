import re
from pkg_resources import load_entry_point

def svn_exception_mask(exception: str):
    masked_line = re.sub(
        "(--username',\s)('.*?')(,\s'--password',\s)('.*?')(.*)",
        r"\1'脱敏处理'\3'脱敏处理'\5", exception, count=1)
    return masked_line


log_str = """{'svn_server': '113.204.226.34', '--username', 'wql', '--password', 'hello', 'svn_url_suffix':"""
print(svn_exception_mask(log_str))

a = re.match('(?P<wanted>[a-zA-Z]*)(?P<not_wanted>[0-9]*)', 'abcefsd123')
if a:
    print(a.groupdict())
