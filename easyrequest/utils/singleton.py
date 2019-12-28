# -*- coding: utf-8 -*-
# @Time    : 2019/03/22 13:51
# @Author  : Liu Yalong
# @File    : singleton.py

# class Singleton:
#     """
#     单例模式 原理：“类变量对所有对象唯一”
#     这种写法，后面的实例属性会覆盖前者的实例属性
#     """
#
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls, '__instance__'):
#             cls.__instance__ = super().__new__(cls)
#         return cls.__instance__


class Meta(type):
    """
    单例模式的metaclass类
    """

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance__'):
            cls.__instance__ = super().__call__(*args, **kwargs)
        return cls.__instance__


class Singleton(metaclass=Meta):
    """这种写法，实例属性是首次创建那个实例的属性"""
    pass
