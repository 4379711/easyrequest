# -*- coding: utf-8 -*-
# @Time    : 2019/11/30 16:29
# @Author  : Liu Yalong
# @File    : __init__.py.py
from gevent import monkey
from easyrequest.entrance.spider_runner import SpiderRunner

monkey.patch_socket()
import gevent
from gevent.pool import Pool


class SpiderEngine:
    def __init__(self, spider, spider_data, mid_cls):
        self.spider = spider
        self.setting = spider.settings
        self.spider_name = spider.spider_name
        self.spider_data = spider_data
        self.mid_cls = mid_cls

    def load_config(self):
        setting = self.spider.settings
        return setting

    def create(self):
        pool = Pool(size=self.setting.CONCURRENT_REQUESTS)
        runner = SpiderRunner(self.spider, self.spider_data, self.mid_cls)

        gevent.joinall([pool.spawn(runner.start, url) for url in self.spider.start_urls])
