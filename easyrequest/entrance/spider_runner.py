# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 11:50
# @Author  : Liu Yalong
# @File    : spider_runner.py
import time
from inspect import isgeneratorfunction
from easyrequest import Request
from easyrequest.utils.log import logger


class SpiderRunner:
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
            print('\033[32mCan not load middleware !\033[0m')
            logger.error('Can not load middleware !')
            return 0

        # create a spider Request instance
        request_instance = self.spider.run()
        if not isinstance(request_instance, Request):
            print('\033[32mReturn Type must be Request in run() !\033[0m')
            logger.error('Return Type must be Request in run() !')
            return 0

        if 0 < retry_times <= self.spider.settings.RETRY_TIMES:
            logger.warning(f'Retry <{retry_times}> : request of url <{url}>')

        if retry_times > self.spider.settings.RETRY_TIMES:
            logger.error(f'retry {retry_times - 1} times still failed ! \n{e}\n\n')
            return 0

        retry_times += 1
        default_config = self._config_request_instance()

        start_time = time.time()
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
                return 0

            # save data
            logger.debug('start save data of url <%s>' % url)

            try:
                self.data_persistence.save(item)
            except Exception as e:
                logger.error(f'save data failed !\n\t\t {e}\n\n')
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

        need_delay_time = self.spider.settings.PER_REQUEST_MIN_TIME
        if time.time() - start_time < need_delay_time:
            time.sleep(time.time() - start_time)
        return 1
