# -*- coding: utf-8 -*-

from easyrequest.items.mydict import MyDict


class MyType:
    """
    Check type of filed .
    """

    def __init__(self, name, expect_type):
        self.expect_type = expect_type
        self.name = name

    def __set__(self, instance, value):
        if self.expect_type and not isinstance(value, self.expect_type):
            raise TypeError(f'Expect <{self.expect_type.__name__}> but got {type(value)}')

        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        if not instance:
            return self
        return instance.__dict__[self.name]

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class StringFiled(MyType):
    def __init__(self, name='StringFiled'):
        super().__init__(name, str)


class IntFiled(MyType):
    def __init__(self, name='IntFiled'):
        super().__init__(name, int)


class DictFiled(MyType):
    def __init__(self, name='DictFiled'):
        super().__init__(name, dict)


class FloatFiled(MyType):
    def __init__(self, name='FloatFiled'):
        super().__init__(name, float)


class DictListFiled(MyType):
    def __init__(self, name='DictListFiled'):
        super().__init__(name, MyDict)


class Filed:
    def __init__(self, name='Filed'):
        # super().__init__(name, None)
        pass
