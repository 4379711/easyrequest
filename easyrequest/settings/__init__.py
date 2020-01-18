# -*- coding: utf-8 -*-

from . import default_settings


class Settings:
    def __init__(self, setting):
        self.update_by_mod(setting)

    def __getitem__(self, item):
        if item not in self.__dict__:
            return None
        return self.__dict__[item]

    def update_by_mod(self, mod):
        self._check_mod(mod)
        for attr in dir(mod):
            if attr.isupper():
                self.__dict__[attr] = getattr(mod, attr)

    def update(self, name, value):
        self.__dict__[name] = value

    def __setitem__(self, name, value):
        if name.isupper():
            self.__dict__[name] = value
        else:
            raise ValueError(f'Can not set {name} ,use {name.upper()} instead !')

    def __contains__(self, name):
        return name in self.__dict__.keys()

    @staticmethod
    def _check_mod(mod):
        if type(mod).__name__ != 'module':
            raise TypeError('Args <mod> must be %s, got %s!' % ('module', type(mod).__name__))

    def __str__(self):
        return '%s Object at %s' % (Settings, Settings.__name__)

    __repr__ = __str__
