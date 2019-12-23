# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 10:00
# @Author  : Liu Yalong
# @File    : __init__.py.py


class LoadError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Can not load %s' % self.name

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
