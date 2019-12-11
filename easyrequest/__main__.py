# -*- coding: utf-8 -*-
# @Time    : 2019/11/12 14:14
# @Author  : Liu Yalong
# @File    : __main__.py
import os
import sys
from colorama import init

init(autoreset=True)

if not __package__:
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)

from easyrequest.cmdline import base_command  # noqa

if __name__ == '__main__':
    base_command()
