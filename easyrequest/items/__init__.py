# -*- coding: utf-8 -*-

from .mydict import MyDict
from .fileds import (
    DictFiled,
    StringFiled,
    IntFiled,
    FloatFiled,
    DictListFiled,
    Filed
)

from abc import abstractmethod, ABC


class Items(ABC):
    """
    Items template .
    """

    @abstractmethod
    def clean(self, items):
        pass

    @abstractmethod
    def save(self, items):
        pass

    @classmethod
    def from_spider(cls):
        spider = cls()
        return spider
