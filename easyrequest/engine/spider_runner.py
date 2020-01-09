# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 11:50
# @Author  : Liu Yalong
# @File    : spider_runner.py
import time
from requests import Response
from inspect import isgeneratorfunction
from easyrequest import Request
from easyrequest.utils.log import logger
from easyrequest.utils.format_print import pprint
from easyrequest.commands import stop_spider


class SpiderRunner:
    """
    Real entrance of a spider .
    """

    def __init__(self, spider_cls, data_cls, mid_cls_list):
        self.spider_cls = spider_cls
        self.data_cls = data_cls
        self.mid_cls_list = mid_cls_list
        self.spider = self._load_spider()
        self.data_persistence = self._load_data_persistence()
        self.middleware_request = self._load_middleware('RequestMiddleWare')
        self.middleware_parse = self._load_middleware('ParserMiddleWare')
        self.default_config = self._config_request_instance()

    def _load_data_persistence(self):
        data_persistence = self.data_cls.from_spider()
        return data_persistence

    def _load_spider(self):
        spider = self.spider_cls.from_spider(self.spider_cls)
        return spider

    def _load_middleware(self, name):
        for mid_cls in self.mid_cls_list:
            if name in mid_cls.__name__:
                return mid_cls

    def _config_request_instance(self):
        # Request configs overwrite settings
        default = {}
        for attr in ['headers', 'timeout', 'verify']:
            default[attr] = self.spider.settings['DEFAULT_REQUEST_' + attr.upper()]
        return default

    def _request(self, func, url=None, retry_times=0, e=None, resp=None):
        if resp is None:
            request_instance = func()
        else:
            request_instance = func(resp)

        if url is None:
            url = request_instance.url

        if not isinstance(request_instance, Request):
            print('\033[32mReturn Type must be Request in run()\nEasyRequest exit !\033[0m')
            logger.error('Return Type must be Request in run() !')
            return

        if 0 < retry_times <= self.spider.settings.RETRY_TIMES:
            logger.warning(f'Retry <{retry_times}> : request of url <{url}>')

        if retry_times > self.spider.settings.RETRY_TIMES:
            logger.error(f'retry {retry_times - 1} times still failed ! \n{e}\n\n')
            pprint(f'retry {retry_times - 1} times still failed ! \n{e}\n\n')
            return

        retry_times += 1

        logger.debug('start request of url <%s>' % url)

        try:
            resp = self.middleware_request(request_instance.request)(url, self.default_config)
            logger.debug('request <%s> finish' % url)

            return resp
        except Exception as e:
            return self._request(func, url, retry_times, e)

    def _continue_request(self, resp):
        if not resp:
            return
        if resp.callback is not None and resp.callback != self.spider.parse_response:
            resp = self._request(resp.callback, resp=resp)
            return self._continue_request(resp)
        else:
            # no callback
            return resp

    def _parse_resp_and_save(self, resp):
        url = resp.url
        logger.debug('Start parse_response of url <%s>' % url)

        if not isgeneratorfunction(self.spider.parse_response):

            try:
                item = self.middleware_parse.from_spider(self.spider.parse_response)(resp)
            except Exception as e:
                logger.error(f'ParseResponse of url <%s> failed !\n\t\t {e}\n\n' % url)
                pprint(f'ParseResponse of url <%s> failed !\n\t\t {e}\n\n' % url)
                return

                # clean data
            logger.debug('Start clean data of url <%s>' % url)
            try:
                items = self.data_persistence.clean(item)
            except Exception as e:
                logger.error(f'Clean data failed !\n\t\t {e}\n\n')
                pprint(f'Clean data failed !\n\t\t {e}\n\n')
                return

                # save data
            logger.debug('Start save data of url <%s>' % url)

            try:
                self.data_persistence.save(items)
            except Exception as e:
                logger.error(f'Save data failed !\n\t\t {e}\n\n')
                pprint(f'Save data failed !\n\t\t {e}\n\n')
                return
        else:
            # if return a generator
            try:
                func_ = self.middleware_parse.from_spider(self.spider.parse_response)

                for item in func_(resp):
                    # save data
                    logger.debug('Start save data of url <%s>' % url)

                    try:
                        self.data_persistence.save(item)
                    except Exception as e:
                        logger.error(f'Save data failed !\n\t\t {e}\n\n')

            except Exception as e:
                logger.error(f'ParseResponse of url <%s> failed !\n\t\t {e}\n\n' % url)
                return 0



    def start(self, url):
        logger.info('Start to request url <%s>' % url)

        # if not isgeneratorfunction(self.spider.run):

        resp = self._request(self.spider.run, url)
        resp = self._continue_request(resp)
        if not isinstance(resp, Response):
            return

        self._parse_resp_and_save(resp)

        time.sleep(self.spider.settings.REQUEST_DELAY)
        logger.info('Request url <%s> finished !' % url)
        return 1
