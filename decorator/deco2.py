"""
把装饰器定义为类
"""

import types
from functools import wraps


class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


@Profiled
def add(x, y):
    return x + y


class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)


def profiled(func):
    """
    使用 nonlocal 变量的替代方案
    """
    ncalls = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal ncalls
        ncalls += 1
        return func(*args, **kwargs)

    wrapper.ncalls = lambda: ncalls
    return wrapper
