# -*- coding: utf-8 -*-
# @Time    : 2020/1/3 10:42
# @Author  : Liu Yalong
# @File    : control_spider.py
from os.path import exists
from subprocess import Popen, PIPE
import psutil
import os
import platform
import signal


def stop_spider(spider_name, path=None):
    if path is None:
        base_path = os.getcwd()
    else:
        base_path = path

    to_read_file = str(spider_name) + '.pid'
    file_path = os.path.join(base_path, to_read_file)
    if not exists(file_path):
        print('spider maybe not running')
        return
    with open(to_read_file, 'r', encoding='utf-8') as f:
        pid = int(f.readline())
        pid_list = psutil.pids()
        if pid not in pid_list:
            print('spider maybe not running')
            return

    os.remove(to_read_file)

    if platform.system() == 'Windows':
        command = f'taskkill /pid {pid} -f'

        pp = Popen(command,
                   shell=True,
                   universal_newlines=True,
                   stdin=PIPE,
                   stderr=PIPE,
                   stdout=PIPE)
        pp.communicate()
    else:
        os.kill(int(pid), signal.SIGKILL)

    # CHECK RESULT
    pid_list = psutil.pids()
    if int(pid) not in pid_list:
        print('stop spider successful')
    else:
        print('stop spider failed')
