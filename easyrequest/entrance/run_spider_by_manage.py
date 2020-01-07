# -*- coding: utf-8 -*-
# @Time    : 2019/12/28 15:47
# @Author  : Liu Yalong
# @File    : run_spider_by_manage.py
from time import sleep
from sys import path
from subprocess import Popen, PIPE
from os.path import join
from os import getcwd

from easyrequest.utils import pprint
from easyrequest.utils.log import logger
from easyrequest.error import ConfigError
from easyrequest.utils.load_module import load_module_from_path
from easyrequest.settings.load_settings import overridden_settings
from easyrequest import schedule

__all__ = ['run_spider_name', 'load_tasks', 'timer_task_by_str']


def run_spider_name(name):
    """
    Run a spider by spider name.
    """
    logger.info(f'<{name}> is about to start !')
    run_command = 'easyrequest RunSpider %s' % name
    process = Popen(run_command,
                    shell=True,
                    universal_newlines=True,
                    stdin=PIPE,
                    stderr=PIPE,
                    stdout=None)
    sleep(1)
    if process.poll() is not None:
        pprint(f' <{name}> crawler process maybe startup failed !')
        logger.error(f'<{name}> crawler process maybe startup failed !')
    process.wait()
    logger.info(f'<{name}> closed !\n\n')


def load_tasks():
    """
    Load timer tasks form settings.py , return command str .
    """
    cmd_path = getcwd()
    path.insert(0, cmd_path)

    # load user config
    user_settings_obj = load_module_from_path('settings.py', join(cmd_path, 'settings.py'))

    # override default config
    settings = overridden_settings(user_settings_obj)
    task_list = settings.TIMER_TASK
    for task in task_list:
        name = task.get('SpiderName')
        every = task.get('every')
        unit = task.get('unit')
        if not (name or every or unit):
            raise ConfigError('TIMER_TASK')
        my_str = f"schedule.every({every}).{unit}.do(run_spider_name, '{name}')"
        yield my_str


def timer_task_by_str(str_):
    """Execute command str"""
    eval(str_)
