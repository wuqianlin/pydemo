class member_table(dict):
    def __init__(self):
        self.member_names = []

    def __setitem__(self, key, value):
        if key not in self:
            self.member_names.append(key)

        dict.__setitem__(self, key, value)


class OrderedClass(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        classdict = member_table()
        print("prepare return dict id is:", id(classdict))
        return classdict

    def __new__(metacls, name, bases, classdict):
        print("new get dict id is:", id(classdict))
        result = type.__new__(metacls, name, bases, dict(classdict))
        result.member_names = classdict.member_names
        print("the class's __dict__ id is:", id(result.__dict__))
        return result

    def __init__(cls, name, bases, classdict):
        print("init get dict id is ", id(classdict))
        super().__init__(name, bases, classdict)


class MyClass(metaclass=OrderedClass):
    def method1(self):
        pass

    def method2(self):
        pass

    print("MyClass locals() id is ", id(locals()))