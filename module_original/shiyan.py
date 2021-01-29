import importlib
# x = importlib.import_module('com_stat_server.notify_plugin.email')
# from com_stat_server.notify_plugin.email import send

# asyncio.run(x.send('data'))


import pkgutil
import sys

def load_all_modules_from_dir(dirname):
    for importer, package_name, _ in pkgutil.iter_modules([dirname], prefix=""):
        full_package_name = '%s' % ('com_stat_server.notify_plugin')
        if full_package_name not in sys.modules:
            module = importer.find_module(package_name)
            print(type(module), module.name, module.path)
            module.load_module()

# load_all_modules_from_dir('/Users/g/Desktop/code/oplatform_server/com_stat_server/notify_plugin')

# print(sys.modules)

import com_stat_server.notify_plugin

for importer, package_name, _ in pkgutil.iter_modules(com_stat_server.notify_plugin.__path__, com_stat_server.notify_plugin.__name__ + '.'):
    importer.find_module(package_name).load_module()


# for importer, package_name, _ in pkgutil.iter_modules(com_stat_server.notify_plugin.__path__, com_stat_server.notify_plugin.__name__ + '.'):
#     module = importer.find_module(package_name)
#     print(module.path)

print(sys.modules)

for attr in dir(com_stat_server.notify_plugin):
    print(attr)


for module in ['.a', '.b']:
    module = importlib.import_module(module, com_stat_server.notify_plugin.__name__)

    for attr in dir(module):
        if not attr.startswith("__"):
            func = getattr(module, attr)
            func()
