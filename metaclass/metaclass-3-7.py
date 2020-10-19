import time

def upper_attr(future_class_name, future_class_parents, future_class_attrs):
    uppercase_attrs = {
        attr if attr.startswith("__") else attr.upper(): v
        for attr, v in future_class_attrs.items()
    }
    return type(future_class_name, future_class_parents, uppercase_attrs)


class UpperAttrMetaclass(type):
    def __new__(cls, clsname, bases, attrs):
        uppercase_attrs = {
            attr if attr.startswith("__") else attr.upper(): v
            for attr, v in attrs.items()
        }
        print('UpperAttrMetaclass: ', cls, clsname, bases, uppercase_attrs)
        ret = super(UpperAttrMetaclass, cls).__new__(cls, clsname, bases, uppercase_attrs)
        print('ret: ', ret)
        return ret


class PrivateAttrMetaclass(metaclass=UpperAttrMetaclass):
    def __new__(cls, clsname, bases, attrs):
        private_attrs = {
            attr if attr.startswith("__") else '_' + attr.upper(): v
            for attr, v in attrs.items()
        }
        print('PrivateAttrMetaclass: ', cls, clsname, bases, private_attrs)
        return super(PrivateAttrMetaclass, cls).__new__(cls, clsname, bases, private_attrs)
        # return type(clsname, bases, private_attrs)
        # return super(PrivateAttrMetaclass, cls).__new__(cls)


class SuffixUnderscoreAttrMetaclass(metaclass=PrivateAttrMetaclass):
    def __new__(cls, clsname, bases, attrs):
        suffix_underscore_attrs = {
            attr if attr.startswith("__") else attr.upper() + '_': v
            for attr, v in attrs.items()
        }
        print('SuffixUnderscore: ', cls, clsname, bases, suffix_underscore_attrs)
        # return super(SuffixUnderscoreAttrMetaclass, cls).__new__(cls, clsname, bases, suffix_underscore_attrs)
        return super(SuffixUnderscoreAttrMetaclass, cls).__new__(cls)


class Foo(metaclass=SuffixUnderscoreAttrMetaclass):
    bar = 'bip'


if __name__ == "__main__":
    print(hasattr(Foo, 'bar'))
    print(hasattr(Foo, '_BAR'))
    print(Foo._BAR_)
