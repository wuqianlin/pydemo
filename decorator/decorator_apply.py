

def call_count(fn):

    def counter(*args, **kwargs):
        counter.__count__ += 1
        print("__")
        return fn(*args, **kwargs)

    counter.__count__ = 0
    return counter

@call_count
def a(): pass

@call_count
def b(): pass

def singleton(cls):
    inst = None

    def wrap(*args, **kwargs):
        nonlocal inst
        if not inst: inst = cls(*args, **kwargs)
        return inst

    return wrap

@singleton
class X: pass

class App:

    def __init__(self):
        self.routers = {}

    def route(self, url):
        def register(fn):
            self.routers[url] = fn
            return fn
        return register

app = App()

@app.route("/")
def index(): pass

@app.route("/help")
def help(): pass

print(app.routers)