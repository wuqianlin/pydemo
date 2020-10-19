"""
我们想编写一个装饰器来包装函数，但是可以让用户调整装饰器的属性，这样在运行时可以控制装饰器的行为。
"""
from functools import wraps, partial
import logging
import time


# A simple decorator
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return r
    return wrapper


# Utility decorator to attach a function as an attribute of obj
def attach_wrapper(obj, func=None):
    print('////  ', obj, func)
    if func is None:
        return partial(attach_wrapper, obj)
    print('////  ', obj, func.__name__, func)
    setattr(obj, func.__name__, func)
    return func


def logged(level, name=None, message=None):
    def decorate(func):
        logname = name if name else func.__name__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        # Attach setter functions
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper
    return decorate


# # Example use
# @logged(logging.DEBUG)
# def add(x, y):
#     return x + y
#
#
# @logged(logging.CRITICAL, 'example')
# def spam():
#     print('Spam!')
