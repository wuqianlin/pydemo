# coding=utf-8
"""
描述符分两种：
    数据描述符：实现了__get__ 和 __set__ 两种方法的描述符
    非数据描述符：只实现了__get__ 一种方法的描述符
数据描述器和非数据描述器的区别在于：它们相对于实例的字典的优先级不同。

如果实例字典中有与描述符同名的属性，如果描述符是数据描述符，优先使用数据描述符，
如果是非数据描述符，优先使用字典中的属性。
"""


# 数据描述符
class DataDes:
    def __init__(self, default=0):
        self._score = default

    def __set__(self, instance, value):
        self._score = value

    def __get__(self, instance, owner):
        print("访问数据描述符里的 __get__")
        return self._score


# 非数据描述符
class NoDataDes:
    def __init__(self, default=0):
        self._score = default

    def __get__(self, instance, owner):
        print("访问非数据描述符里的 __get__")
        return self._score


class Student:
    math = DataDes(0)
    chinese = NoDataDes(0)

    def __init__(self, name, math, chinese):
        self.name = name
        self.math = math
        self.chinese = chinese

    def __getattribute__(self, item):
        print("调用 __getattribute__")
        return super(Student, self).__getattribute__(item)

    def __repr__(self):
        return "<Student: {}, math:{}, chinese: {},>".format(
            self.name, self.math, self.chinese)


if __name__ == "__main__":
    std = Student('xm', 88, 99)
    print(std.math)    # 数据描述符
    print('_.' * 20)
    print(std.chinese)    # 非数据描述符
