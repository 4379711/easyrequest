# -*- coding: utf-8 -*-
# @Time    : 2019/12/28 15:47
# @Author  : Liu Yalong
# @File    : run_spider_by_manage.py
from subprocess import Popen, PIPE
from easyrequest.utils.log import logger
import time
from easyrequest.error import ConfigError
from easyrequest.utils.load_module import load_module_from_path
import os
from os.path import join
import sys
from easyrequest.settings.load_settings import overridden_settings

__all__ = ['run_spider_name', 'load_tasks', 'timer_task_by_str']


def run_spider_name(name):
    logger.info(f'定时器启动任务{name}')
    run_command = 'easyrequest RunSpider %s' % name
    process = Popen(run_command,
                    shell=True,
                    universal_newlines=True,
                    stdin=PIPE,
                    stderr=PIPE,
                    stdout=None)
    while True:
        time.sleep(1)
        pid = process.pid
        logger.info(f'子进程pid:{pid}')
        if process.poll() is not None:
            logger.info(f'子进程启动失败')
        _, b = process.communicate()
        if b:
            logger.error(f'子进程发生错误')
        logger.info(f'定时器关闭任务{name}')


def load_tasks():
    cmd_path = os.getcwd()
    sys.path.insert(0, cmd_path)

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
    eval(str_)
