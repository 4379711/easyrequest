# -*- coding: utf-8 -*-
# @Time    : 2019/12/30 17:10
# @Author  : Liu Yalong
# @File    : __init__.py.py
import types
from abc import abstractmethod, ABC
from inspect import isgeneratorfunction
from functools import wraps


class BaseMiddleWares(ABC):
    @abstractmethod
    def before(self, *args, **kwargs):
        pass

    @abstractmethod
    def after(self, *args, **kwargs):
        pass


class RequestMiddleWares(BaseMiddleWares):
    def __init__(self, func):
        wraps(func)(self)
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    def __call__(self, config):
        try:
            self.before(config)
            result = self.func(config)
            self.after()
            return result
        except Exception as e:
            self.exception(e, config)
            raise e

    @abstractmethod
    def exception(self, error, params):
        pass

    @classmethod
    def from_spider(cls, func):
        return cls(func)

    def __str__(self):
        return '%s Object at %s' % (RequestMiddleWares, RequestMiddleWares.__name__)

    __repr__ = __str__


class ParserMiddleWares(BaseMiddleWares):
    def __init__(self, func):
        wraps(func)(self)
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    def __call__(self, resp):
        if isgeneratorfunction(self.func):

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
        else:

            try:
                self.before(resp)
                result = self.func(resp)
                self.after(resp)
                yield result
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


class MixFuncGeneratorMiddleWare:
    """
    Change function to a generator function .
    """

    def __init__(self, func):
        wraps(func)(self)
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        if isgeneratorfunction(self.func):

            gen_tmp = self.func(*args, **kwargs)
            try:
                while True:
                    result = next(gen_tmp)
                    yield result
            except StopIteration:
                raise StopIteration
            except Exception as e:
                raise e
        else:

            try:
                result = self.func(*args, **kwargs)
                yield result
            except Exception as e:
                raise e
