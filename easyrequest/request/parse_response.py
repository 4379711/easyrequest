# -*- coding: utf-8 -*-
# @Time    : 2019/12/21 17:32
# @Author  : Liu Yalong
# @File    : parse_response.py
import re
import lxml.etree


class Parser:

    def __init__(self, html):
        self.html = html
        self.tree = lxml.etree.HTML(html)

    def by_re(self, rule, flags=0):
        aa = re.findall(rule, self.html, flags)
        return aa

    def by_xpath(self, rule, **kwargs):
        aa = self.tree.xpath(rule, **kwargs)
        return aa
