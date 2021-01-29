import os
import importlib

def get_modules(package="."):
    """
    获取包名下所有非__init__的模块名
    """
    modules = []
    files = os.listdir(package)

    for file in files:
        if not file.startswith("__"):
            name, ext = os.path.splitext(file)
            modules.append("." + name)

    return modules


if __name__ == '__main__':
    package = "clazz"
    modules = get_modules(package)
    print(modules)

    # 将包下的所有模块，逐个导入，并调用其中的函数
    for module in modules:
        module = importlib.import_module(module, package)
        print(module)

        for attr in dir(module):
            if not attr.startswith("__"):
                func = getattr(module, attr)
                func()
