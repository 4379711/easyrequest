# -*- coding: utf-8 -*-

from easyrequest.commands import base_command
import sys


def execute():
    base_command()
    sys.exit(0)


if __name__ == '__main__':
    execute()
