"""过 __getattr__ 方法，实现非侵入式编程"""


class Fjs(object):
    def __init__(self, name):
        self.name = name

    def hello(self):
        print("said by : ", self.name)

    # def __getattribute__(self, item):
    #     print("访问了特性：" + item)
    #     return object.__getattribute__(self, item)

    def fjs(self, name):
        if name == self.name:
            print('yes')
        else:
            print('no')


class Wrap_Fjs(object):
    def __init__(self, fjs):
        self._fjs = fjs

    def __getattribute__(self, item):
        print(f'__getattribute__: {item}')
        return object.__getattribute__(self, item)

    def __getattr__(self, item):
        """这里通过 __getattr__ 方法，将所有的特性的访问都路由给了内部的fjs对象"""
        if item == 'hello':
            print('调用hello方法了')
        elif item == 'fjs':
            print('调用fjs方法了')
        return getattr(self._fjs, item)


fjs = Wrap_Fjs(Fjs('fjs'))
fjs.hello()
fjs.fjs('fjs')
