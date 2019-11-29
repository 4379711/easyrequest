# -*- coding: utf-8 -*-
# @Time    : 2019/11/29 9:21
# @Author  : Liu Yalong
# @File    : create_spider.py
from __future__ import print_function
import re
import os
from os.path import join, exists, abspath
from shutil import copyfile

from easyrequest.utils.template import render_template_file, string_camelcase

import easyrequest

must_exists = {'settings.py', 'manage.py', 'apps'}


class CommandSpider:

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
        file_list = set(os.listdir(cmd_path))
        if len(must_exists - file_list) > 0:
            print(f"\033[32mError: Project don't exists,create project command:\033[0m")
            print('    EasyRequest CreateProject xxx')
            return
        spider_file_name = f'{spider_name}.py'

        if exists(join(cmd_path, 'apps', spider_file_name)):
            print(f'\033[32mError: Spider "{spider_name}" already exists in %s\033[0m')
            return
        src_name = join(self.templates_file, 'spider.py.template')
        dst_name = join(abspath(cmd_path), 'apps', f'{spider_name}.py.template')
        copyfile(src_name, dst_name)
        render_template_file(dst_name, classname=string_camelcase(spider_name))

        print("\033[32mCreate Spider '%s finished in:' " % spider_file_name)
        print("    %s\033[0m" % join(abspath(cmd_path), 'apps', spider_file_name))

    @property
    def templates_file(self):
        # 模板路径
        _templates_base_dir = join(easyrequest.__path__[0], 'templates')
        return join(_templates_base_dir, 'app')
