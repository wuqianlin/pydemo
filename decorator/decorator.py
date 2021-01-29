import functools


def log(fn):
    def wrap(*args, **kwargs):
        print(f"log: {args}, {kwargs}")
        return fn(*args, **kwargs)

    return wrap


class LogClass:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        print(f"log: {args}, {kwargs}")
        return self.fn(*args, **kwargs)


def log_with_argument(name="default"):
    print(f"args: {name}")

    def decorator(fn):
        print(f"decorator: {fn}")
        return fn

    return decorator


def log_like_origin(fn):
    @functools.wraps(fn)
    def wrap(*args, **kwargs):
        return fn(*args, **kwargs)

    print(f"wrap: {id(wrap)}, func: {id(fn)}")
    return wrap


def log_for_class(cls):
    class wrapper:
        def __init__(self, *args, **kwargs):
            self.__dict__['inst'] = cls(*args, **kwargs)

        def __getattr__(self, name):
            value = getattr(self.inst, name)
            print(f"get: {name} = {value}")
            return value

        def __setattr__(self, name, value):
            print(f"set: {name} = {value}")
            return setattr(self.inst, name, value)

    return wrapper


def log_return_instance(cls):
    def wrap(*args, **kwargs):
        o = cls(*args, **kwargs)
        print(f"log: {o}")
        return o

    return wrap


@log_like_origin
def add(x: int, y: int) -> int:
    return x + y


@log_for_class
class X: pass


@log_return_instance
class X: pass


X()
