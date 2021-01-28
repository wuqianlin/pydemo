from multiprocessing import Process, Manager
from collections import defaultdict


def f(d, l):
    a = defaultdict(list)
    a['a'].append('fuck')
    d['fuck'] = a
    print(d)
    l.reverse()


if __name__ == '__main__':
    with Manager() as manager:
        _d = manager.dict()
        _l = manager.list(range(10))

        p = Process(target=f, args=(_d, _l))
        p.start()
        p.join()

        print(_d['fuck'], type(_d['fuck']))
        print(_l)
