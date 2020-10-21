class OBJ(object):
    def __new__(self, a):
        ins = object.__new__(OBJ)
        print("call OBJ new with parameter %s, created inst %s" %  (a, ins))
        # return ins # 去掉这行就不会再调用__init__

    def __init__(self, a):
        print("call OBJ new with parameter %s, inst %s" %  (a, self))


if __name__ == '__main__':
    OBJ(123)