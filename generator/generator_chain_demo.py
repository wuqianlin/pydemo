#!/usr/bin/python
import itertools
from functools import reduce
from itertools import tee


def foo1(g):
    for i in g:
        yield i + 1


def foo2(g):
    for i in g:
        yield 10 + i


def foo3(g):
    for i in g:
        yield 'foo3:' + str(i)


def foo4(g):
    for i in g:
        yield 'foo4:' + str(i)
        yield 'foo5:' + str(i)



# res = foo3(foo2(foo1(range(0, 5))))
# for i in res:
#     print(i)


def compose(*funcs):
    return lambda x: reduce(lambda f, g: g(f), list(funcs), x)


p = compose(foo1, foo2)
bb = p(range(0, 5))
c, d = tee(bb, 2)

ee = compose(foo3)
ff = compose(foo4)

gg = ee(c)
hh = ff(d)

for x in hh:
    print(x)