import pkgutil
import sys


def load_all_modules_from_dir(dirname):
    for importer, package_name, _ in pkgutil.iter_modules([dirname], prefix='xxx'):
        full_package_name = '%s.%s' % (dirname, package_name)
        print(importer, package_name, _)
        if full_package_name not in sys.modules:
            module = importer.find_module(package_name)
            print(type(module), dir(module))
            module.load_module()
            # print(module)


load_all_modules_from_dir('clazz')
print(sys.modules['a'])

import module_demo.clazz.a
