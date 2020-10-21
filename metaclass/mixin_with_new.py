import inspect


class RunImp(object):
    def run(self):
        print('just run')


class FlyImp(object):
    def fly(self):
        print('just fly')


class MetaMixinEx(type):
    def __new__(cls, name, bases, dic):
        member_list = (RunImp, FlyImp)

        for imp_member in member_list:
            if not imp_member:
                continue

            for method_name, fun in inspect.getmembers(imp_member, inspect.isfunction):
                print('class %s get method %s from %s' % (name, method_name, imp_member))
                assert method_name not in dic, (imp_member, method_name)
                dic[method_name] = fun
        return type.__new__(cls, name, bases, dic)


class Bird(object, metaclass=MetaMixinEx):
    pass


class SpecialBird(Bird):
    pass
