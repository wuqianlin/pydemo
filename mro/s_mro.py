
class A(object):
    def __init__(self):
        print("enter A")
        print("leave A")


class B(object):
    def __init__(self):
        print("enter B")
        print("leave B")


class C(A):
    def __init__(self):
        print("enter C")
        super(C, self).__init__()
        print("leave C")


class D(A):
    def __init__(self):
        print("enter D")
        super(D, self).__init__()
        print("leave D")


class E(B, C):
    def __init__(self):
        print("enter E")
        B.__init__(self)
        C.__init__(self)
        print("leave E")


class F(E, D):
    def __init__(self):
        print("enter F")
        E.__init__(self)
        D.__init__(self)
        print("leave F")


f = F()
"""
请写出输出内容，并作出解释。
正确的输出应该是：
enter F
enter E
enter B
leave B
enter C
enter D
enter A
leave A
leave D
leave C
leave E
enter D
enter A
leave A
leave D
leave F
"""

