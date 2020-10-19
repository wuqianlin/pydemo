class Meta(type):
    def __new__(mcs, *args, **kwargs):
        print('+')
        ins = super().__new__(mcs, *args, **kwargs)
        ins.xxx = 'xxx'
        return ins


class MyClass(metaclass=Meta):
    pass


class MySubclass(MyClass):
    pass


class MySubSubclass(MySubclass):
    pass


print(MyClass.xxx)
print(MySubclass.xxx)
print(MySubSubclass.xxx)

print(isinstance(MyClass, type))
print(isinstance(MySubclass, type))
print(isinstance(MySubSubclass, type))