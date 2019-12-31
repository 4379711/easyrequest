# -*- coding: utf-8 -*-
# @Time    : 2019/12/19 11:11
# @Author  : Liu Yalong
# @File    : spider.py
from abc import abstractmethod, ABC

from easyrequest.error import LoadError


class CrawlSpider(ABC):
    start_urls = []

    def __init__(self, start_urls=None, **kwargs):
        if start_urls is not None:
            self.start_urls = start_urls
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def parse_response(self, response):
        pass

    @classmethod
    def from_spider(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._config_crawler(crawler)
        return spider

    def _config_crawler(self, crawler):
        self.crawler = crawler
        if not hasattr(crawler, 'settings'):
            raise LoadError('settings')
        self.settings = crawler.settings
