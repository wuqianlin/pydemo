"""
source information come from url:
https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python/100037#100037

A metaclass is the class of a class. A class defines how an instance of the class (i.e. an object)
behaves while a metaclass defines how a class behaves. A class is an instance of a metaclass.

While in Python you can use arbitrary callables for metaclasses (like Jerub shows), the better
approach is to make it an actual class itself. type is the usual metaclass in Python. type is
itself a class, and it is its own type. You won't be able to recreate something like type purely
in Python, but Python cheats a little. To create your own metaclass in Python you really just want to
subclass type.

A metaclass is most commonly used as a class-factory. When you create an object by calling the class,
Python creates a new class (when it executes the 'class' statement) by calling the metaclass.
Combined with the normal __init__ and __new__ methods, metaclasses therefore allow you to do 'extra things'
when creating a class, like registering the new class with some registry or replace the class
with something else entirely.

When the class statement is executed, Python first executes the body of the class statement
as a normal block of code. The resulting namespace (a dict) holds the attributes of the class-to-be.
The metaclass is determined by looking at the baseclasses of the class-to-be (metaclasses are inherited),
at the __metaclass__ attribute of the class-to-be (if any) or the __metaclass__ global variable.
The metaclass is then called with the name, bases and attributes of the class to instantiate it.

However, metaclasses actually define the type of a class, not just a factory for it,
so you can do much more with them. You can, for instance, define normal methods on the metaclass.
These metaclass-methods are like classmethods in that they can be called on the class without an instance,
but they are also not like classmethods in that they cannot be called on an instance of the class.
type.__subclasses__() is an example of a method on the type metaclass.
You can also define the normal 'magic' methods, like __add__, __iter__ and __getattr__,
to implement or change how the class behaves.
"""


def make_hook(f):
    """Decorator to turn 'foo' method into '__foo__'"""
    f.is_hook = 1
    return f


class MyType(type):
    def __new__(mcs, name, bases, attrs):

        if name.startswith('None'):
            return None

        # Go over attributes and see if they should be renamed.
        newattrs = {}
        for attrname, attrvalue in attrs.iteritems():
            if getattr(attrvalue, 'is_hook', 0):
                newattrs['__%s__' % attrname] = attrvalue
            else:
                newattrs[attrname] = attrvalue

        return super(MyType, mcs).__new__(mcs, name, bases, newattrs)

    def __init__(self, name, bases, attrs):
        super(MyType, self).__init__(name, bases, attrs)

        # classregistry.register(self, self.interfaces)
        print "Would register class %s now." % self

    def __add__(self, other):
        class AutoClass(self, other):
            pass
        return AutoClass
        # Alternatively, to autogenerate the classname as well as the class:
        # return type(self.__name__ + other.__name__, (self, other), {})

    def unregister(self):
        # classregistry.unregister(self)
        print "Would unregister class %s now." % self


class MyObject:
    __metaclass__ = MyType


class NoneSample(MyObject):
    pass


# Will print "NoneType None"
print 'Source Type: ', type(NoneSample), repr(NoneSample)


class Example(MyObject):
    def __init__(self, value):
        self.value = value

    @make_hook
    def add(self, other):
        return self.__class__(self.value + other.value)


# Will unregister the class
Example.unregister()

inst = Example(10)
# Will fail with an AttributeError
#inst.unregister()

print 'add:', inst + inst


class Sibling(MyObject):
    pass


ExampleSibling = Example + Sibling
# ExampleSibling is now a subclass of both Example and Sibling (with no
# content of its own) although it will believe it's called 'AutoClass'
print 'ExampleSibling:', ExampleSibling
print 'ExampleSibling.__mro__: ', ExampleSibling.__mro__
