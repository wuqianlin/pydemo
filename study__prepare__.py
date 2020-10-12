
class member_table(dict):

    def __init__(self):
        print(f"which id: {id(self)}")
        self.member_names = []

    def __setitem__(self, key, value):
        # if the key is not already defined, add to the
        # list of keys.
        if key not in self:
            self.member_names.append(key)

        dict.__setitem__(self, key, value)


class OrderedClass(type):
    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        """used to create the namespace for the class statement"""
        classdict =member_table()
        print(f'prepare accept kwargs: {kwargs}')
        print('prepare return dict id is:', id(classdict))
        return classdict

    def __new__(metacls, name, bases, classdict, **kwargs):
        # Note that we replace the classdict with a regular
        # dict before passing it to the superclass, so that we
        # don't continue to record member names after the class
        # has been created.
        print("new get dict id is:", id(classdict))
        result = type.__new__(metacls, name, bases, dict(classdict))
        result.member_names = classdict.member_names
        print("the class's __dict__ id is:", id(result.__dict__))
        return result

    def __init__(cls, name, bases, classdict, **kwargs):
        print("init get dict id is ", id(classdict))
        super().__init__(name, bases, classdict)


class MyClass(metaclass=OrderedClass, a=1, b=2):

    def method1(self):
        pass

    def method2(self):
        pass

    print("MyClass locals() id is ", id(locals()))


"""
输出：
    prepare return dict id is: 4538334768
    MyClass locals() id is  4538334768
    new get dict id is: 4538334768
    the class's __dict__ id is: 4536430160
    init get dict id is  4538334768
    可见，执行顺序为：prepare（创建命名空间）-> 依次执行类定义语句 -> new（创建类）-> init（初始化类）
    元类定义了prepare以后，会最先执行prepare方法，返回一个空的定制的字典，然后再执行类的语句，
    类中定义的各种属性被收集入定制的字典，最后传给new和init方法。
再来看其它输出：
    In [4]: MyClass.member_names                                                                                                                       
    Out[4]: ['__module__', '__qualname__', 'method1', 'method2']
    In [6]: MyClass.attr1 = 'attr1'                                                                                                                    
    In [7]: MyClass.__dict__                                                                                                                           
    Out[7]: 
    mappingproxy({'__module__': 'study__prepare__',
                  'method1': <function study__prepare__.MyClass.method1(self)>,
                  'method2': <function study__prepare__.MyClass.method2(self)>,
                  '__dict__': <attribute '__dict__' of 'MyClass' objects>,
                  '__weakref__': <attribute '__weakref__' of 'MyClass' objects>,
                  '__doc__': None,
                  'member_names': ['__module__',
                   '__qualname__',
                   'method1',
                   'method2'],
                  'attr1': 'attr1'})
             
    In [8]: id(MyClass.__dict__)   
    Out[8]: 4538660496

    In [9]: id(MyClass.__dict__)                                                                                                                       
    Out[9]: 4537976464
    
    In [10]: id(MyClass.__dict__)                                                                                                                      
    Out[10]: 4537527696
    
    In [11]: MyClass.member_names                                                                                                                      
    Out[11]: ['__module__', '__qualname__', 'method1', 'method2']
    
    上面的例子，在new方法中，dict被替换成一个普通的dict。所以MyClass.member_names不会记录class创建以后新增的属性。
    同时__dict__属性是类命名空间的一个代理，每次查看其id都不同。3.6版本以前，prepare方法主要用来返回一个orderdict对象，
    以保存类中属性的添加顺序。而3.6版本以后，默认已经是保持顺序的了。
"""