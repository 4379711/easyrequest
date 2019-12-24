# -*- coding: utf-8 -*-
# @Time    : 2019/12/21 13:38
# @Author  : Liu Yalong
# @File    : request.py
from requests import api


class Request:

    def __init__(self, method='GET', data_pass=None, **kwargs):
        self.method = method
        self.kwargs = kwargs
        self.data_pass = data_pass

    def request(self, url):
        resp = api.request(method=self.method, url=url, **self.kwargs)
        resp.data_pass = self.data_pass
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
