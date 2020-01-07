# -*- coding: utf-8 -*-
import re
import os
from importlib import import_module
from os.path import join, exists, abspath
from shutil import ignore_patterns, copy2, copystat
from easyrequest.utils.template import MyTemplate, render_template_file, string_camelcase
import easyrequest

IGNORE = ignore_patterns('*.pyc', '.svn', '*.pyi', '__pycache__')
TEMPLATES_TO_RENDER = (
    ('>>{project_name}', 'settings.py.template'),
)


class CommandProject:

    @staticmethod
    def _is_valid_name(project_name):
        def _module_exists(module_name):
            try:
                import_module(module_name)
                return True
            except ImportError:
                return False

        if not re.search(r'^[_a-zA-Z]\w*$', project_name):
            print('\033[32mError: Project names must begin with a letter and contain only\n'
                  'letters, numbers and underscores\033[0m')
        elif _module_exists(project_name):
            print('\033[32mError: Module %r already exists\033[0m' % project_name)
        else:
            return True
        return False

    def _copytree(self, src, dst):
        ignore = IGNORE
        names = os.listdir(src)
        ignored_names = ignore(src, names)

        if not os.path.exists(dst):
            os.makedirs(dst)

        for name in names:
            if name in ignored_names:
                continue

            src_name = os.path.join(src, name)
            dst_name = os.path.join(dst, name)
            if os.path.isdir(src_name):
                self._copytree(src_name, dst_name)
            else:
                copy2(src_name, dst_name)
        copystat(src, dst)

    def run(self, project_name):

        # 新建的project存放路径
        project_dir = os.getcwd()

        if exists(join(project_dir, project_name)):
            print('\033[32mError: EasyRequest project already exists in %s\033[0m' % abspath(project_dir))
            return

        if not self._is_valid_name(project_name):
            return

        self._copytree(self.templates_dir, join(abspath(project_dir), project_name))

        for paths in TEMPLATES_TO_RENDER:
            path = join(*paths)
            tpl_file = join(project_dir, MyTemplate(path).substitute(project_name=project_name))
            render_template_file(tpl_file, project_name=project_name, ProjectName=string_camelcase(project_name))

        print("Create Project '%s in:' " % project_name)
        print("    %s\n" % abspath(project_dir))

        print("You can start your first spider with:")
        print("    \033[32mcd %s\033[0m" % str(project_name))
        print("    \033[32mEasyRequest CreateSpider first_spider\033[0m")

    @property
    def templates_dir(self):
        # 模板路径
        _templates_base_dir = join(easyrequest.__path__[0], 'templates')
        return join(_templates_base_dir, 'projects')
