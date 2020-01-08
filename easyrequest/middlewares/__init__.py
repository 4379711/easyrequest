# -*- coding: utf-8 -*-
# @Time    : 2019/12/30 17:10
# @Author  : Liu Yalong
# @File    : __init__.py.py
from abc import abstractmethod, ABC


class BaseMiddleWares(ABC):
    @abstractmethod
    def before(self, *args, **kwargs):
        pass

    @abstractmethod
    def after(self, *args, **kwargs):
        pass


class RequestMiddleWares(BaseMiddleWares):
    def __init__(self, func):
        self.func = func

    def __call__(self, url, config):
        try:
            self.before(url, config)
            result = self.func(url, config)
            self.after(url)
            return result
        except Exception as e:
            self.exception(e, url, config)
            raise e

    @abstractmethod
    def exception(self, error, url, params):
        pass

    @classmethod
    def from_spider(cls, func):
        return cls(func)

    def __str__(self):
        return '%s Object at %s' % (RequestMiddleWares, RequestMiddleWares.__name__)

    __repr__ = __str__


class ParserMiddleWares(BaseMiddleWares):
    def __init__(self, func):
        self.func = func

    def __call__(self, resp):
        gen_tmp = self.func(resp)
        try:
            self.before(resp)
            while True:
                result = next(gen_tmp)
                self.after(resp)
                yield result
        except StopIteration:
            raise StopIteration
        except Exception as e:
            self.exception(e, resp)
            raise e

    @abstractmethod
    def exception(self, error, resp):
        pass

    @classmethod
    def from_spider(cls, func):
        return cls(func)

    def __str__(self):
        return '%s Object at %s' % (ParserMiddleWares, ParserMiddleWares.__name__)

    __repr__ = __str__
