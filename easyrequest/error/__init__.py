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
