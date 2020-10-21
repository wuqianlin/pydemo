from functools import wraps
import logging


def logged(a, b=None):
    def decorate(func):
        print(f'收到参数：{a}, {b}')
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("in deep func")
            return func(*args, **kwargs)
        return wrapper
    return decorate


@logged(a=1)
def add(x, y):
    return x + y


add(5, 6)
