# -*- coding: utf-8 -*-

from os.path import exists
from subprocess import Popen, PIPE
import psutil
import os
import platform
import signal
import time


def stop_spider(spider_name, path=None):
    """
    Stop a running spider .
    """
    if path is None:
        base_path = os.getcwd()
    else:
        base_path = path

    to_read_file = str(spider_name) + '.pid'
    file_path = os.path.join(base_path, to_read_file)

    if not exists(file_path):
        print('Spider maybe not running or you forget to set [ RECORD_PID= True ] in setting.py !')
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        pid = int(f.readline())
        pid_list = psutil.pids()
        if pid not in pid_list:
            print('Spider maybe not running !')
            return

    os.remove(file_path)

    # signal can only be used on linux .
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
        print('\tStop spider successful !')
    else:
        print('\tStop spider maybe failed !')
