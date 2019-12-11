# -*- coding: utf-8 -*-
# @Time    : 2019/12/10 16:54
# @Author  : Liu Yalong
# @File    : start_spider.py
from __future__ import print_function

import re
import os
from os.path import join, exists
from easyrequest.settings.load_settings import overridden_settings
from easyrequest.utils.format_print import pprint


from importlib import import_module

from easyrequest.utils.load_module import load_module_from_path


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

        spider_file_name = f'{spider_name}.py'

        if not exists(join(cmd_path, 'apps', spider_file_name)):
            print(f'\033[32mError: Spider "{spider_name}" not exists\033[0m')
            return

        if not exists(join(cmd_path, 'settings.py')):
            print(f'\033[32mError: Check that your project path is correct! \033[0m')
            pprint('You must execute the RunSpider command in the project directory')
            return

        # 加载用户配置
        user_settings_obj = load_module_from_path('settings.py', join(cmd_path, 'settings.py'))

        # 覆盖默认配置
        tmp_ = overridden_settings(user_settings_obj)
        for k in tmp_:
            print(k)
