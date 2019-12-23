# -*- coding: utf-8 -*-
# @Time    : 2019/11/30 16:29
# @Author  : Liu Yalong
# @File    : __init__.py.py
from gevent import monkey

monkey.patch_socket()
import gevent
from gevent.pool import Pool

from easyrequest.entrance.spider_runner import SpiderRunner


class SpiderEngine:
    def __init__(self, spider):
        self.spider = spider
        self.setting = spider.settings

    def load_config(self):
        setting = self.spider.settings
        return setting

    def create(self):
        pool = Pool(size=self.setting.CONCURRENT_REQUESTS)
        runner = SpiderRunner(self.spider)

        gevent.joinall([pool.spawn(runner.start, url) for url in self.spider.start_urls])
