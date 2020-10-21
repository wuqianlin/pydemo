"""
'most pythonic' way to achieve singleton.
https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
https://blog.konghy.cn/2017/08/06/new-init-singleton/
使用 python __new__ 方法实现单例
"""


class Singleton(object):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class A(Singleton):
    pass


a = A()
b = A()


print(f"id(a) equal id(b): {id(a) == id(b)}")


"""
使用 decorator 方法实现单例
"""
import inspect


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class BaseClass:
    pass


@singleton
class MyClass(BaseClass):
    pass


e = MyClass()
f = MyClass()

print(f"MyClass is a function: {inspect.isfunction(MyClass)}")
print(f"id(e) equal id(f): {id(e) == id(f)}")


class Meta(type):
    def __new__(cls, *args, **kwargs):
        print('come here')
        return super().__new__(cls, *args, **kwargs)


class Foo(object, metaclass=Meta):

    def __new__(cls, m, n):
        print(cls, m, n)
        print("__new__ is called")
        return super(Foo, cls).__new__(cls)

    def __init__(self, m, n):
        print("__init__ is called")
        self.m = m
        self.n = n

    def __repr__(self):
        return f"Foo(m={self.m}, n={self.n})"

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    f = Foo(1, 2)
    print(f)
