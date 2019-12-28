# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 10:00
# @Author  : Liu Yalong
# @File    : __init__.py.py


class LoadError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Can not load %s ,Check spider file <Apps.xxx.py , Models.xxxItems.py> is correct !' % self.name

    __repr__ = __str__


class ReturnTypeError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Return Type must be %s ' % self.name.__name__

    __repr__ = __str__


class ParameterError(Exception):
    def __init__(self, whos, name):
        self.name = name
        self.whos = whos

    def __str__(self):
        return '%s parameter must be %s ' % (self.whos.__name__, self.name.__name__)

    __repr__ = __str__


class RetryError(Exception):
    def __init__(self, times, url, err):
        self.url = url
        self.times = times
        self.err = err

    def __str__(self):
        return 'Request <%s> Retry <%d> times still failed ,error:\n\n       %s' % (self.url, self.times, self.err)

    __repr__ = __str__


class ConfigError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Error of %s config in settings' % self.name

    __repr__ = __str__
