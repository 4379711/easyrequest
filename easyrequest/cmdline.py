# -*- coding: utf-8 -*-
# @Time    : 2019/11/13 11:52
# @Author  : Liu Yalong
# @File    : cmdline.py
from easyrequest.commands import base_command
import sys


def execute():
    base_command()
    sys.exit(0)


if __name__ == '__main__':
    execute()
