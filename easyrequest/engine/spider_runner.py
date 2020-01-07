# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 11:50
# @Author  : Liu Yalong
# @File    : spider_runner.py
import time
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

    def start(self, url, retry_times=0, e=None):
        try:
            middleware_request = self._load_middleware('RequestMiddleWare')
            middleware_parse = self._load_middleware('ParserMiddleWare')
        except Exception:
            print('\033[32mCan not load middleware \nEasyRequest exit !\033[0m')
            logger.error('Can not load middleware !')
            stop_spider(self.spider.spider_name)
            return 0

        # create a spider Request instance
        request_instance = self.spider.run()
        if not isinstance(request_instance, Request):
            print('\033[32mReturn Type must be Request in run()\nEasyRequest exit !\033[0m')
            logger.error('Return Type must be Request in run() !')
            return 0

        if 0 < retry_times <= self.spider.settings.RETRY_TIMES:
            logger.warning(f'Retry <{retry_times}> : request of url <{url}>')

        if retry_times > self.spider.settings.RETRY_TIMES:
            logger.error(f'retry {retry_times - 1} times still failed ! \n{e}\n\n')
            pprint(f'retry {retry_times - 1} times still failed ! \n{e}\n\n')
            return 0

        retry_times += 1
        default_config = self._config_request_instance()

        logger.info('start request url <%s>' % url)
        logger.debug('start request of url <%s>' % url)

        try:
            resp = middleware_request(request_instance.request)(url, default_config)
        except Exception as e:
            return self.start(url, retry_times, e)

        logger.debug('start parse_response of url <%s>' % url)

        if not isgeneratorfunction(self.spider.parse_response):

            try:
                item = middleware_parse.from_spider(self.spider.parse_response)(resp)
            except Exception as e:
                logger.error(f'ParseResponse of url <%s> failed !\n\t\t {e}\n\n' % url)
                pprint(f'ParseResponse of url <%s> failed !\n\t\t {e}\n\n' % url)
                return 0

            # clean data
            logger.debug('start clean data of url <%s>' % url)
            try:
                items = self.data_persistence.clean(item)
            except Exception as e:
                logger.error(f'clean data failed !\n\t\t {e}\n\n')
                pprint(f'clean data failed !\n\t\t {e}\n\n')
                return 0

            # save data
            logger.debug('start save data of url <%s>' % url)

            try:
                self.data_persistence.save(items)
            except Exception as e:
                logger.error(f'save data failed !\n\t\t {e}\n\n')
                pprint(f'save data failed !\n\t\t {e}\n\n')
                return 0

        else:
            # if return a generator , can not catch exception in middleware

            print('\033[32mparse_response can not be generator !\033[0m')
            logger.error('parse_response can not be generator !')
            return 0
            # try:
            #     func_ = middleware_parse.from_spider(self.spider.parse_response)
            #
            #     for item in func_(resp):
            #         # save data
            #         logger.debug('start save data of url <%s>' % url)
            #
            #         try:
            #             self.data_persistence.save(item)
            #         except Exception as e:
            #             logger.error(f'save data failed !\n\t\t {e}\n\n')
            #
            # except Exception as e:
            #     logger.error(f'ParseResponse of url <%s> failed !\n\t\t {e}\n\n' % url)
            #     return 0

        logger.info('request <%s> finish' % url)

        time.sleep(self.spider.settings.REQUEST_DELAY)

        return 1
