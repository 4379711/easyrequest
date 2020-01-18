# -*- coding: utf-8 -*-

import re
import lxml.etree


class Parser:
    """
    Parse html .
    """

    def __init__(self, html):
        self.html = html
        self.tree = lxml.etree.HTML(html)

    def by_re(self, rule, flags=0):
        aa = re.findall(rule, self.html, flags)
        return aa

    def by_xpath(self, rule, **kwargs):
        aa = self.tree.xpath(rule, **kwargs)
        return aa
