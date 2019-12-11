# -*- coding: utf-8 -*-
# @Time    : 2019/12/10 16:13
# @Author  : Liu Yalong
# @File    : loads.py
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec


def load_object(path):
    """Load an object given its absolute object path, and return it.

    object can be a class, function, variable or an instance.
    path ie: 'easyrequest.settings.default_settings'

    Example:
    >>> tmp =load_object('easyrequest.settings.default_settings')
    >>> tmp.DEFAULT_REQUEST_HEADERS
    {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en'}
    """

    try:
        dot = path.rindex('.')

    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj


def load_module_from_path(name, location):
    aa = module_spec = spec_from_file_location(name, location)
    if aa is None:
        raise AttributeError(f"Can not find module {name} in {location}")

    module = module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


if __name__ == '__main__':
    load_object('easyrequest.settings.default_settings')
