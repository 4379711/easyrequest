# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 11:50
# @Author  : Liu Yalong
# @File    : spider_runner.py
from easyrequest import Request
from easyrequest.error import ReturnTypeError


class SpiderRunner:
    def __init__(self, spider_cls, data_cls):
        self.spider_cls = spider_cls
        self.spider = self.load_spider()

        self.data_cls = data_cls

    def load_spider(self):
        spider = self.spider_cls.from_spider(self.spider_cls)
        return spider

    def start(self, url):
        request = self.spider.run()
        if not isinstance(request, Request):
            raise ReturnTypeError(Request)

        # if request.callback is not None and not callable(request.callback):
        #     raise ParameterError(Request, callable)

        # start request http://www.xxx.com
        resp = request.request(url=url)

        item = self.spider.parse_response(resp)

        # save data
        self.data_cls.save(item)

        # if resp
        # def deal_callback(resp_=resp):
        #     if resp_.callback is not None and request.callback.__name__ == 'parse_response':
        #         other_resp = resp_.callback(resp_)
        #         return deal_callback(resp_=other_resp)
        #     return default_callback(resp_)
        #
        # deal_callback(resp)
