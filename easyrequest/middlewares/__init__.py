# -*- coding: utf-8 -*-
# @Time    : 2019/12/30 17:10
# @Author  : Liu Yalong
# @File    : __init__.py.py
from abc import abstractmethod


class MiddleWares:
    def __init__(self):
        pass

    @abstractmethod
    def before(self):
        pass

    @abstractmethod
    def end(self):
        pass

    @classmethod
    def from_spider(cls):
        return cls()
