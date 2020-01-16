# -*- coding: utf-8 -*-
# @Time    : 2019/11/28 16:47
# @Author  : Liu Yalong
# @File    : __init__.py.py
import re
import os
import sys
from hashlib import md5
from os.path import join, exists
from threading import Lock
from collections import defaultdict

from easyrequest.error import RequestUrl
from .format_print import pprint
from .load_module import *


def average_number_of_groups(m, n):
    """
    把一个数据分割为近似大小的N份

    :param m: 待分割的数据总长度
    :param n: 需要分为几份
    :return: 返回列表,代表应该分割的下标+1
    """

    base_num = m // n
    over_num = m % n

    result = [base_num for _ in range(n)]

    for i in range(over_num):
        result[i] = result[i] + 1

    for i in range(n - 1):
        result[i + 1] = result[i] + result[i + 1]

    return result


def split_urls_by_group(urls, n):
    aa = average_number_of_groups(len(urls), n)

    for i in range(len(aa)):
        if i == 0:
            yield (urls[:aa[i]])
        else:
            yield (urls[aa[i - 1]:aa[i]])


def write_process_pid(spider_name):
    # record process id to file
    base_path = os.getcwd()
    to_write_file = str(spider_name) + '.pid'
    file_path = os.path.join(base_path, to_write_file)
    pid = os.getpid()
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(pid))
        f.flush()


def check_spider_name(spider_name):
    if not re.search(r'^[_a-zA-Z]\w*$', spider_name):
        print('\033[32mError: spider names must begin with a letter and contain only\n'
              'letters, numbers and underscores\033[0m')
        return False
    else:
        return True


def check_project_file(spider_name):
    cmd_path = os.getcwd()
    sys.path.insert(0, cmd_path)

    spider_file_name = f'{spider_name}.py'

    if not exists(join(cmd_path, 'Apps', spider_file_name)):
        print(f'\033[32mError: Spider "{spider_name}" not exists\033[0m')
        return False

    if not exists(join(cmd_path, 'settings.py')):
        print(f'\033[32mError: Check that your project path is correct! \033[0m')
        pprint('You must execute the RunSpider command in the project directory')
        return False
    return True


def get_md5(url, kwargs):
    if not isinstance(url, str):
        raise RequestUrl
    md5_str = md5((url + str(kwargs)).encode('utf-8')).hexdigest()
    return md5_str


class RecordTaskInfo:

    def __init__(self):
        self._all_request = set()
        self._all_parse = set()
        self._request = 0
        self._request_failed = 0
        self._parse_failed = 0
        self._success = 0
        self._lock0 = Lock()
        self._lock4 = Lock()
        self._lock1 = Lock()
        self._lock2 = Lock()
        self._lock5 = Lock()

    def request_add(self, value):
        with self._lock0:
            self._all_request.add(value)

    def parse_add(self, value):
        with self._lock4:
            self._all_parse.add(value)

    def request_failed_plus(self):
        with self._lock1:
            self._request_failed += 1

    def parse_failed_plus(self):
        with self._lock5:
            self._parse_failed += 1

    def success_plus(self):
        with self._lock2:
            self._success += 1

    def is_in_set(self, value):
        return value in self._all_request

    @property
    def info(self):
        return self._request, self._success, self._request_failed, self._parse_failed
