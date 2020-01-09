# -*- coding: utf-8 -*-
# @Time    : 2019/12/21 13:38
# @Author  : Liu Yalong
# @File    : request.py
from requests import api


class Request:
    """
    Request a url .
    """

    def __init__(self,
                 url=None,
                 method='GET',
                 data_pass=None,
                 callback=None,
                 **kwargs):
        self.method = method
        self.kwargs = kwargs
        self.data_pass = data_pass
        self.callback = callback
        self.url = url

    def request(self, url=None, config=None):
        if self.url is None:
            self.url = url
        config.update(self.kwargs)
        resp = api.request(method=self.method,
                           url=self.url,
                           **config)
        resp.data_pass = self.data_pass
        resp.callback = self.callback
        return resp

    @staticmethod
    def get(url, params=None, data_pass=None, callback=None, **kwargs):
        resp = api.get(url, params=params, **kwargs)
        resp.data_pass = data_pass
        resp._callback = callback
        return resp

    @staticmethod
    def post(url, data=None, json=None, data_pass=None, callback=None, **kwargs):
        resp = api.post(url, data=data, json=json, **kwargs)
        resp.data_pass = data_pass
        resp._callback = callback
        return resp
