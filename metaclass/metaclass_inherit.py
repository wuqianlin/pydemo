"""
metaclass 在多重继承如何使用

Python metaclass behavior (not calling __new__), is there an explanation?
https://stackoverflow.com/questions/28465955/python-metaclass-behavior-not-calling-new-is-there-an-explanation

仔细阅读文档 https://docs.python.org/3.7/reference/datamodel.html#determining-the-appropriate-metaclass 可以
解释下边程序的输出：
The appropriate metaclass for a class definition is determined as follows:
    1. if no bases and no explicit metaclass are given, then type() is used;
    2. if an explicit metaclass is given and it is not an instance of type(),
    then it is used directly as the metaclass;
    3. if an instance of type() is given as the explicit metaclass, or bases
    are defined, then the most derived metaclass is used.
The most derived metaclass is selected from the explicitly specified metaclass (if any)
and the metaclasses (i.e. type(cls)) of all specified base classes. The most
derived metaclass is one which is a subtype of all of these candidate metaclasses.
If none of the candidate metaclasses meets that criterion, then the class definition
will fail with TypeError.
"""


class A(type):
    def __new__(mcs, name, bases, dct):
        print("mcs  :", mcs)
        print("name :", name)
        print("bases:", bases)
        print("dct  :", dct)
        ins = super(A, mcs).__new__(mcs, name, bases, dct)
        print(f'Metaclass is an instance of, A: {isinstance(ins, A)}, type: {isinstance(ins, type)} \n')
        return ins


class B(metaclass=A):
    pass


class C(B):
    pass


class N(C):
    pass


print(type(B))
print(type(C))
print(type(N), '\n')


class D(type):
    def __new__(mcs, name, bases, dct):
        print("mcs  :", mcs)
        print("name :", name)
        print("bases:", bases)
        print("dct  :", dct)
        ins = type(name, bases, dct)
        print(f'Metaclass is an instance of, D: {isinstance(ins, D)}, type: {isinstance(ins, type)} \n')
        return ins


class E(metaclass=D):
    print('Inside class E, type(D):', type(D), '\n')
    pass


class F(E):
    print('Inside class F: type(E):', type(E))
    pass


"""
>>> from metaclass_inherit import *
mcs  : <class '__main__.A'>
name : B
bases: ()
dct  : {'__module__': '__main__', '__qualname__': 'B'}
Metaclass is an instance of, A: True, type: True 

mcs  : <class '__main__.A'>
name : C
bases: (<class '__main__.B'>,)
dct  : {'__module__': '__main__', '__qualname__': 'C'}
Metaclass is an instance of, A: True, type: True 

mcs  : <class '__main__.A'>
name : N
bases: (<class '__main__.C'>,)
dct  : {'__module__': '__main__', '__qualname__': 'N'}
Metaclass is an instance of, A: True, type: True 

<class '__main__.A'>
<class '__main__.A'>
<class '__main__.A'> 

Inside class E, type(D): <class 'type'> 

mcs  : <class '__main__.D'>
name : E
bases: ()
dct  : {'__module__': '__main__', '__qualname__': 'E'}
Metaclass is an instance of, D: False, type: True 

Inside class F: type(E): <class 'type'>
"""


"""
原因解释：
In the second case instead of returning an instance of the metaclass you're actually 
returning an instance of type, this in turn sets the __class__ attribute of the newly 
created class E as <type 'type'> instead of D. Hence [as per the rule 2] Python checks 
for base class's __class__ attribute(or type(E) or E.__class__) and decides to use 
type as F's metaclass, so D's __new__ is never called in this case.

在第二个状况中，class D(type) 返回了 type 的实例（<class 'type'>）而不是metaclass D 的实例，
这造成了新创建的类 E.__class__ 属性为 <class 'type'> 而不是 <class 'D'>。 参照官方文档
[Determining the appropriate metaclass](https://docs.python.org/3.7/reference/
datamodel.html#determining-the-appropriate-metaclass) 第三条规则，类 F 会使用 E.__class__ 属性
或者 type(E) 的值来决定类 F 的 metaclass， 因此 D 的 __new__ 函数永远也不会执行。
"""