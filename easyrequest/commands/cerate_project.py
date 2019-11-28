# -*- coding: utf-8 -*-
# @Time    : 2019/11/28 16:44
# @Author  : Liu Yalong
# @File    : cerate_project.py
from __future__ import print_function
import re
import os
import string
from importlib import import_module
from os.path import join, exists, abspath
from shutil import ignore_patterns, move, copy2, copystat
from easyrequest.utils.template import render_templatefile, string_camelcase
import easyrequest

TEMPLATES_TO_RENDER = (
    ('scrapy.cfg',),
    ('${project_name}', 'settings.py.tmpl'),
    ('${project_name}', 'items.py.tmpl'),
    ('${project_name}', 'pipelines.py.tmpl'),
    ('${project_name}', 'middlewares.py.tmpl'),
)

IGNORE = ignore_patterns('*.pyc', '.svn', '*.pyi')


class Command:

    @staticmethod
    def _is_valid_name(project_name):
        def _module_exists(module_name):
            try:
                import_module(module_name)
                return True
            except ImportError:
                return False

        if not re.search(r'^[_a-zA-Z]\w*$', project_name):
            print('Error: Project names must begin with a letter and contain only\nletters, numbers and underscores')
        elif _module_exists(project_name):
            print('Error: Module %r already exists' % project_name)
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

            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            if os.path.isdir(srcname):
                self._copytree(srcname, dstname)
            else:
                copy2(srcname, dstname)
        copystat(src, dst)

    def run(self, project_name):

        project_dir = os.getcwd()

        if exists(join(project_dir, 'flag.py')):
            print('Error: EasyRequest project already exists in %s' % abspath(project_dir))
            return

        if not self._is_valid_name(project_name):
            return

        self._copytree(self.templates_dir, abspath(project_dir))
        move(join(project_dir, 'modules'), join(project_dir, project_name))
        for paths in TEMPLATES_TO_RENDER:
            path = join(*paths)
            tplfile = join(project_dir, string.Template(path).substitute(project_name=project_name))
            render_templatefile(tplfile, project_name=project_name, ProjectName=string_camelcase(project_name))
        print("New project '%s', using template directory '%s', "
              "created in:" % (project_name, self.templates_dir))
        print("    %s\n" % abspath(project_dir))

        print("You can start your first spider with:")
        print("    cd %s" % project_dir)
        print("    EasyRequest CreateProject example")

    @property
    def templates_dir(self):
        _templates_base_dir = join(easyrequest.__path__[0], 'templates')
        return join(_templates_base_dir, 'projects')
