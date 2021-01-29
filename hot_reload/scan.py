import time
from importlib import reload

from plugins import plugin

method_list = ['avg', 'total', 'last', 'unknown', 'moon', 'flower', 'dynamic']
while True:
    reload(plugin)
    for f in method_list:
        if hasattr(plugin, f):
            _f = getattr(plugin, f)
            _result = _f()
            print(_result)
        else:
            print(f'未找到方法{f}')
    print("\n")
    time.sleep(2)
