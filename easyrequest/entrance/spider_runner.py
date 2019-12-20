# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 11:50
# @Author  : Liu Yalong
# @File    : spider_runner.py
from gevent import monkey

from easyrequest.request.spider import CrawlSpider

monkey.patch_socket()
import gevent
from requests import api


class SpiderRunner:
    def __init__(self, spider_cls):
        self.spider_cls = spider_cls

    def load_spider(self):
        spider = CrawlSpider.from_spider(self.spider_cls)
        return spider

