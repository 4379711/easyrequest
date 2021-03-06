# -*- coding: utf-8 -*-

import re
import os
import sys
from hashlib import md5
from os.path import join, exists
from threading import Lock

from easyrequest.error import RequestUrl
from .format_print import pprint
from .load_module import *


def average_number_of_groups(m, n):
    """
    Split a data into N parts of approximate size .

    :param m: Total length of data to be split .
    :param n: Need to be divided into several portions .
    :return: list ,index +1 that should be split .
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
        # self._all_request = set()
        # self._all_parse = set()

        self._all_request = []

        self._request_success = 0
        self._request_failed = 0
        self._parse_success = 0
        self._parse_failed = 0
        self._save_failed = 0
        self._save_success = 0

        self._lock0 = Lock()
        self._lock1 = Lock()
        self._lock2 = Lock()
        self._lock3 = Lock()
        self._lock4 = Lock()
        self._lock5 = Lock()
        self._lock6 = Lock()
        self._lock7 = Lock()

    # When _all_request is a set() .

    # def request_add(self, value):
    #     with self._lock0:
    #         self._all_request.add(value)

    # def parse_add(self, value):
    #     with self._lock1:
    #         self._all_parse.add(value)

    def request_add(self, value):
        with self._lock0:
            self._all_request.append(value)

    def parse_add(self, value):
        with self._lock0:
            self._all_request.remove(value)

    def request_success_plus(self):
        with self._lock2:
            self._request_success += 1

    def request_failed_plus(self):
        with self._lock3:
            self._request_failed += 1

    def parse_success_plus(self):
        with self._lock4:
            self._parse_success += 1

    def parse_failed_plus(self):
        with self._lock5:
            self._parse_failed += 1

    def save_failed_plus(self):
        with self._lock6:
            self._save_failed += 1

    def save_success_plus(self):
        with self._lock7:
            self._save_success += 1

    def is_in_set(self, value):
        return value in self._all_request

    # @property
    # def two_set_same(self):
    #     return self._all_request == self._all_parse

    @property
    def requests_is_empty(self):
        return self._all_request == []

    @property
    def info(self):
        return (self._request_success,
                self._request_failed,
                self._parse_success,
                self._parse_failed,
                self._save_success,
                self._save_failed
                )
