# -*- coding: utf-8 -*-
# @Time    : 2019/12/10 16:54
# @Author  : Liu Yalong
# @File    : start_spider.py
import re
import os
from os.path import join, exists
import sys

from easyrequest.engine import SpiderEngine
from easyrequest.error import LoadError
from easyrequest.items import Items
from easyrequest.request.spider import CrawlSpider
from easyrequest.settings.load_settings import overridden_settings
from easyrequest.utils.format_print import pprint

from easyrequest.utils.load_module import load_cls_from_module, load_module_from_path


class CommandStartSpider:

    @staticmethod
    def _is_valid_name(spider_name):

        if not re.search(r'^[_a-zA-Z]\w*$', spider_name):
            print('\033[32mError: spider names must begin with a letter and contain only\n'
                  'letters, numbers and underscores\033[0m')
            return False
        else:
            return True

    def run(self, spider_name):
        if not self._is_valid_name(spider_name):
            return

        cmd_path = os.getcwd()
        sys.path.insert(0, cmd_path)

        spider_file_name = f'{spider_name}.py'

        if not exists(join(cmd_path, 'apps', spider_file_name)):
            print(f'\033[32mError: Spider "{spider_name}" not exists\033[0m')
            return

        if not exists(join(cmd_path, 'settings.py')):
            print(f'\033[32mError: Check that your project path is correct! \033[0m')
            pprint('You must execute the RunSpider command in the project directory')
            return

        # load user config
        user_settings_obj = load_module_from_path('settings.py', join(cmd_path, 'settings.py'))

        # override default config
        settings = overridden_settings(user_settings_obj)

        # load spider cls
        spider_module = load_module_from_path(spider_name, join(cmd_path, join('Apps', spider_file_name)))
        iter_spider_cls = load_cls_from_module(spider_module, sub_class=CrawlSpider)
        spclasses = list(iter_spider_cls)

        spider_data_file_name = f'{spider_name}_data_persistence.py'
        # load spider data persistence
        spider_data_module = load_module_from_path(spider_name,
                                                   join(cmd_path, join('DataPersistence', spider_data_file_name)))
        iter_spider_data_cls = load_cls_from_module(spider_data_module, sub_class=Items)
        spider_data_cls = list(iter_spider_data_cls)

        # ############
        spider_middleware_name = f'{spider_name}_middleware.py'
        # load spider middleware
        spider_middleware_module = load_module_from_path(spider_name,
                                                         join(cmd_path, join('Middlewares', spider_middleware_name)))
        iter_middleware_cls = load_cls_from_module(spider_middleware_module, sub_class=Items)
        spider_middleware_cls = list(iter_middleware_cls)

        if not spclasses or not spider_data_cls or not spider_middleware_cls:
            raise LoadError(spider_name)

        spider_cls = spclasses.pop()
        # set spider config
        spider_cls.settings = settings

        spider_data_cls = spider_data_cls.pop()

        engine = SpiderEngine(spider_cls, spider_data_cls)
        engine.create()
