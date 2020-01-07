# -*- coding: utf-8 -*-
# @Time    : 2020/1/7 14:53
# @Author  : Liu Yalong
# @File    : load_all_modules.py
import os
from os.path import join
from easyrequest.middlewares import BaseMiddleWares
from easyrequest.items import Items
from easyrequest.request.spider import CrawlSpider
from easyrequest.settings.load_settings import overridden_settings
from easyrequest.utils.load_module import load_cls_from_module, load_module_from_path


class LoadAllModules:

    def __init__(self, spider_name):
        self.spider_name = spider_name
        self.cmd_path = os.getcwd()

    def load_user_config(self):
        # load user config
        user_settings_obj = load_module_from_path('settings.py', join(self.cmd_path, 'settings.py'))

        # override default config
        settings = overridden_settings(user_settings_obj)
        return settings

    def load_spider_cls(self):
        # load spider cls
        spider_file_name = f'{self.spider_name}.py'
        spider_module = load_module_from_path(self.spider_name, join(self.cmd_path, join('Apps', spider_file_name)))
        iter_spider_cls = load_cls_from_module(spider_module, sub_class=CrawlSpider)
        sp_classes = list(iter_spider_cls)
        return sp_classes

    def load_data_persistence_cls(self):
        spider_data_file_name = f'{self.spider_name}_data_persistence.py'
        spider_data_module = load_module_from_path(self.spider_name,
                                                   join(self.cmd_path, join('DataPersistence', spider_data_file_name)))
        iter_spider_data_cls = load_cls_from_module(spider_data_module, sub_class=Items)
        spider_data_cls = list(iter_spider_data_cls)
        return spider_data_cls

    def load_middleware_cls(self):
        spider_middleware_name = f'{self.spider_name}_middleware.py'
        spider_middleware_module = load_module_from_path(
            self.spider_name, join(self.cmd_path, join('Middlewares', spider_middleware_name)))
        iter_middleware_cls = load_cls_from_module(spider_middleware_module, sub_class=BaseMiddleWares)
        spider_middleware_cls_list = list(iter_middleware_cls)
        return spider_middleware_cls_list
