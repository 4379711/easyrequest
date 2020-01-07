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
import time


def stop_spider(spider_name, path=None):
    if path is None:
        base_path = os.getcwd()
    else:
        base_path = path

    to_read_file = str(spider_name) + '.pid'
    file_path = os.path.join(base_path, to_read_file)

    if not exists(file_path):
        print('Spider maybe not running !')
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        pid = int(f.readline())
        pid_list = psutil.pids()
        if pid not in pid_list:
            print('Spider maybe not running !')
            return

    os.remove(file_path)

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
        os.killpg(os.getpgid(int(pid)), signal.SIGKILL)

    print('Checking result ...\n')
    time.sleep(0.5)
    # CHECK RESULT
    pid_list = psutil.pids()
    if int(pid) not in pid_list:
        print('Stop spider successful !')
    else:
        print('Stop spider maybe failed !')
