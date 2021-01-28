def deco_a(tag: str):
    print(tag)

    def dec2(cls):
        print('deco_a', cls)
        cls.attr_a = 100
        return cls

    return dec2


def deco_b(cls):
    print('deco_b', cls)
    return cls


@deco_a("I am Model")
class Model(object):
    test_val = 0

    def __init__(self):
        pass


@deco_b
class SubModel(Model):
    def __init__(self):
        print(type(self))
        pass


if __name__ == '__main__':
    model = SubModel()
    # print(model.attr_a)
