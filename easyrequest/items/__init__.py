# -*- coding: utf-8 -*-
# @Time    : 2019/12/23 15:26
# @Author  : Liu Yalong
# @File    : __init__.py.py
from .mydict import MyDict
from .fileds import (
    DictFiled,
    StringFiled,
    IntFiled,
    FloatFiled,
    DictListFiled,
    Filed
)

from abc import abstractmethod


class Items:
    @abstractmethod
    def save(self, items):
        pass
