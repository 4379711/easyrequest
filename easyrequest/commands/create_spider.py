# -*- coding: utf-8 -*-
# @Time    : 2019/11/29 9:21
# @Author  : Liu Yalong
# @File    : create_spider.py
from __future__ import print_function
import re
import os
from os.path import join, exists, abspath
from shutil import copyfile
import easyrequest

must_exists = {'settings', 'manage.py', 'apps'}


class CommandSpider:

    @staticmethod
    def _is_valid_name(spider_name):

        if not re.search(r'^[_a-zA-Z]\w*$', spider_name):
            print('Error: spider names must begin with a letter and contain only\nletters, numbers and underscores')
            return False
        else:
            return True

    def run(self, spider_name):
        if not self._is_valid_name(spider_name):
            return

        cmd_path = os.getcwd()
        file_list = set(os.listdir(cmd_path))
        if len(must_exists - file_list) > 0:
            print(f"Error: Project don't exists,create project command:")
            print('    EasyRequest CreateProject xxx')
            return
        spider_file_name = f'{spider_name}.py'

        if exists(join(cmd_path, 'apps', spider_file_name)):
            print(f'Error: Spider "{spider_name}" already exists in %s')
            return

        copyfile(self.templates_file, join(abspath(cmd_path), 'apps', spider_file_name))
        print("Create Spider '%s in:' " % spider_file_name)
        print("    %s\n" % join(abspath(cmd_path), 'apps', spider_file_name))

    @property
    def templates_file(self):
        # 模板路径
        _templates_base_dir = join(easyrequest.__path__[0], 'templates')
        return join(_templates_base_dir, 'app', 'spider')
