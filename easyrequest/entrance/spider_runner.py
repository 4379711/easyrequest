# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 11:50
# @Author  : Liu Yalong
# @File    : spider_runner.py
import time

from easyrequest import Request
from easyrequest.error import ReturnTypeError, RetryError


class SpiderRunner:
    def __init__(self, spider_cls, data_cls):
        self.spider_cls = spider_cls
        self.data_cls = data_cls
        self.spider = self._load_spider()
        self.data_persistence = self._load_data_persistence()

    def _load_data_persistence(self):
        data_persistence = self.data_cls.from_spider()
        return data_persistence

    def _load_spider(self):
        spider = self.spider_cls.from_spider(self.spider_cls)
        return spider

    def _config_request_instance(self):
        # Request configs overwrite settings
        default = {}
        for attr in ['headers', 'timeout', 'verify']:
            default[attr] = self.spider.settings['DEFAULT_REQUEST_' + attr.upper()]
        return default

    def start(self, url, retry_times=0, e=None):
        print(f'开始第{retry_times}次请求{url}\n\n')
        request_instance = self.spider.run()
        if not isinstance(request_instance, Request):
            raise ReturnTypeError(Request)

        if retry_times > self.spider.settings.RETRY_TIMES:
            raise RetryError(retry_times - 1, url, e)

        retry_times += 1
        default_config = self._config_request_instance()

        start_time = time.time()
        try:
            # start request http://www.xxx.com
            resp = request_instance.request(url=url, config=default_config)
        except Exception as e:
            return self.start(url, retry_times, e)

        item = self.spider.parse_response(resp)

        # save data
        self.data_persistence.save(item)

        time.sleep(self.spider.settings.REQUEST_DELAY)

        need_delay_time = self.spider.settings.PER_REQUEST_MIN_TIME
        if time.time() - start_time < need_delay_time:
            time.sleep(time.time() - start_time)
