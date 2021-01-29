import itertools
import threading


def generator():
    for i in range(1000000):
        yield i


x = sum(generator())
print(x)

g = generator()
g1, g2 = itertools.tee(g, 2)
for x in [g1, g2]:
    threading.Thread(target=sum, args=(x, )).start()
