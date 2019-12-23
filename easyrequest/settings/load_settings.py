# -*- coding: utf-8 -*-
# @Time    : 2019/12/10 16:31
# @Author  : Liu Yalong
# @File    : load_settings.py
from easyrequest.settings import default_settings, Settings


def iter_default_settings():
    """Return the default settings as an iterator of (name, value) tuples"""

    for name in dir(default_settings):
        if name.isupper():
            yield name, getattr(default_settings, name)


def overridden_settings(settings):
    """Return a dict of the settings that have been overridden"""

    settings = Settings(settings)
    for name, dft_value in iter_default_settings():
        value = settings[name]
        if value != dft_value and value is not None:
            settings.update(name, value)
        elif value is None:
            settings.update(name, dft_value)
    return settings
