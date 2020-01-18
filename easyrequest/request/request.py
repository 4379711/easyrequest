# -*- coding: utf-8 -*-

from requests import api
import urllib3
from easyrequest.utils import get_md5

urllib3.disable_warnings()


class Request:
    """
    Request a url .
    """

    def __init__(self,
                 url=None,
                 method='GET',
                 data_pass=None,
                 callback=None,
                 is_filter=True,
                 **kwargs):
        self.method = method
        self.kwargs = kwargs
        self.data_pass = data_pass
        self.callback = callback
        self.url = url
        self.is_filter = is_filter
        self.md5 = get_md5(self.url, self.kwargs)

    def request(self, config=None):
        config.update(self.kwargs)
        resp = api.request(method=self.method,
                           url=self.url,
                           **config)
        resp.data_pass = self.data_pass
        resp.callback = self.callback
        resp.md5 = self.md5
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
