# -*- coding: utf-8 -*-
# @Time    : 2019/11/29 9:21
# @Author  : Liu Yalong
# @File    : create_spider.py
import os
from os.path import join, exists, abspath
from shutil import copyfile

from easyrequest.utils.template import render_template_file, string_camelcase
from easyrequest.utils import check_spider_name

import easyrequest

must_exists = {'settings.py', 'manage.py', 'Models', 'Apps', 'DataPersistence'}


class CommandSpider:

    def run(self, spider_name):
        if not check_spider_name(spider_name):
            return

        cmd_path = os.getcwd()
        file_list = set(os.listdir(cmd_path))
        if len(must_exists - file_list) > 0:
            print(f"\033[32mError: Project don't exists,create project command:\033[0m")
            print('    EasyRequest CreateProject xxx')
            return
        spider_file_name = f'{spider_name}.py'

        if exists(join(cmd_path, 'Apps', spider_file_name)):
            print(f'\033[32mError: Spider "{spider_name}" already exists \033[0m')
            return

        items_name = f'{spider_name}_items'
        # create spider file
        src_name = join(self.templates_file, 'spider.py.template')
        dst_name = join(abspath(cmd_path), 'Apps', f'{spider_name}.py.template')
        copyfile(src_name, dst_name)
        render_template_file(dst_name,
                             classname=string_camelcase(spider_name),
                             itemname=items_name,
                             itemclassname=string_camelcase(items_name)
                             )

        # create items file
        src_name = join(self.templates_file, 'items.py.template')

        dst_name = join(abspath(cmd_path), 'Models', f'{items_name}.py.template')
        copyfile(src_name, dst_name)
        render_template_file(dst_name, classname=string_camelcase(items_name))

        # create data persistence file
        data_persistence_name = f'{spider_name}_data_persistence'

        src_name = join(self.templates_file, 'data_persistence.py.template')

        dst_name = join(abspath(cmd_path), 'DataPersistence', f'{data_persistence_name}.py.template')
        copyfile(src_name, dst_name)
        render_template_file(dst_name, classname=string_camelcase(data_persistence_name))

        # create middleware file
        middleware_name = f'{spider_name}_middleware'

        src_name = join(self.templates_file, 'middleware.py.template')

        dst_name = join(abspath(cmd_path), 'Middlewares', f'{middleware_name}.py.template')
        copyfile(src_name, dst_name)
        render_template_file(dst_name, classname=string_camelcase(spider_name))

        print("\033[32mCreate Spider '%s finished in:' " % spider_name)
        print("    %s\033[0m" % abspath(cmd_path))

    @property
    def templates_file(self):
        # 模板路径
        _templates_base_dir = join(easyrequest.__path__[0], 'templates')
        return join(_templates_base_dir, 'app')
