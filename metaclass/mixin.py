import inspect
import types


class RunImp(object):
    def run(self):
        print('just run')


class FlyImp(object):
    def fly(self):
        print('just fly')


class MetaMixin(type):
    def __init__(cls, name, bases, dic):
        super(MetaMixin, cls).__init__(name, bases, dic)
        member_list = (RunImp, FlyImp)

        for imp_member in member_list:
            if not imp_member:
                continue

            for method_name, fun in inspect.getmembers(imp_member, inspect.isfunction):
                print('class %s get method %s from %s' % (name, method_name, imp_member))
                # assert not hasattr(cls, method_name), method_name
                setattr(cls, method_name, fun)


class Bird(object, metaclass=MetaMixin):
    pass


class DummyMetaIMixin(MetaMixin):
    def __init__(cls, name, bases, dic):
        type.__init__(cls, name, bases, dic)


class SpecialBird(Bird, metaclass=DummyMetaIMixin):
    pass


# class SpecialBird(Bird):
#     def run(self):
#         print('SpecialBird run')


if __name__ == '__main__':
    b = SpecialBird()
    b.run()

