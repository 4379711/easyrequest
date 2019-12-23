# -*- coding: utf-8 -*-
# @Time    : 2019/12/21 17:32
# @Author  : Liu Yalong
# @File    : parse_response.py
import re


class Parser:

    def __init__(self, response):
        self.response = response

    def by_re(self, rule):
        aa = re.findall(rule, self.response)
        return aa
