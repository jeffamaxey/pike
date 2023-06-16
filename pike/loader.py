import os
import sys
import imp


class PikeLoader(object):
    def __init__(self, fullname, module_path):
        self.target_module_name = fullname
        self.module_path = module_path

    def is_package(self, fullname=None):
        """
        :param fullname: Not used, but required for Python 3.4
        """

        filename = os.path.basename(self.module_path)
        return filename.startswith('__init__')

    def augment_module(self, fullname, module):
        package, _, _ = fullname.rpartition('.')

        if self.is_package():
            module.__path__ = [self.module_path]
            module.__package__ = fullname
        else:
            module.__package__ = package

        return module

    def load_module(self, fullname):
        if self.target_module_name != fullname:
            raise ImportError('Cannot import module with this loader')

        if fullname in sys.modules:
            return sys.modules[fullname]

        module = self.load_module_by_path(fullname, self.module_path)

        sys.modules[fullname] = module
        return module

    def load_module_by_path(self, module_name, path):
        _, ext = os.path.splitext(path)
        module = imp.load_source(module_name, path) if ext.lower() == '.py' else None
        if module:
            # Make sure we properly fill-in __path__ and __package__
            module = self.augment_module(module_name, module)

        return module
