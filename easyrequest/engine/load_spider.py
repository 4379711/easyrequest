# -*- coding: utf-8 -*-
# @Time    : 2019/11/30 17:19
# @Author  : Liu Yalong
# @File    : load_spider.py

from easyrequest.settings import default_settings
from importlib import import_module

class LoadSpider:

    def load(self):
        print(import_module(default_settings))

LoadSpider().load()