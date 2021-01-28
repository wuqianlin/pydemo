from multiprocessing import Process, Value, Lock
from multiprocessing.managers import BaseManager


class Employee(object):
    def __init__(self, name, salary):
        self.name = name
        self.salary = Value('i', salary)

    def increase(self):
        self.salary.value += 100

    def get_pay(self):
        return self.name + ':' + str(self.salary.value)


class CustomManager(BaseManager):
    pass


CustomManager.register('Employee', Employee)


def create_multi_manager():
    m = CustomManager()
    m.start()
    return m


def func1(_em, _lock):
    with _lock:
        _em.increase()


if __name__ == '__main__':
    manager = create_multi_manager()
    em = manager.Employee('ZhangSan', 1000)
    lock = Lock()
    processes = [ Process(target=func1, args=(em, lock)) for i in range(10) ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print( em.get_pay() )