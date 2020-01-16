# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 11:50
# @Author  : Liu Yalong
# @File    : spider_runner.py
import time
from easyrequest import Request
from easyrequest.engine import record_task_info
from easyrequest.utils.log import logger
from easyrequest.utils.format_print import pprint


class SpiderRunner:
    """
    Real entrance of a spider .
    """

    def __init__(self, pool, spider_cls, data_cls, mid_cls_list, task_sender):
        self.pool = pool
        self.spider_cls = spider_cls
        self.data_cls = data_cls
        self.mid_cls_list = mid_cls_list
        self.spider = self._load_spider()
        self.data_persistence = self._load_data_persistence()
        self.middleware_request = self._load_middleware('RequestMiddleWare')
        self.middleware_parse = self._load_middleware('ParserMiddleWare')
        self.default_config = self._config_request_instance()
        self.task_sender = task_sender

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

    def _parse_resp_and_save_by_generator(self, resp):
        url = resp.url
        logger.debug('Start parse_response of url <%s>' % url)
        try:
            func_ = self.middleware_parse.from_spider(self.spider.parse_response)

            for item in func_(resp):
                # save data
                logger.debug('Start save data of url <%s>' % url)

                try:
                    self.data_persistence.save(item)
                except Exception as e:
                    pprint(f'Save data failed !\n\t\t {e}\n\n')
                    logger.error(f'Save data failed !\n\t\t {e}\n\n')
                    record_task_info.parse_failed_plus()

        except Exception as e:
            logger.error(f'ParseResponse of url <%s> failed !\n\t\t {e}\n\n' % url)
            record_task_info.parse_failed_plus()
            return 0

    def _request(self, request_instance, retry_times=0, e=None, resp=None):
        if not isinstance(request_instance, Request):
            print('\033[32mReturn Type must be Request in run()\nEasyRequest exit !\033[0m')
            logger.error('Return Type must be Request in run() !')

            return

        url = request_instance.url

        if 0 < retry_times <= self.spider.settings.RETRY_TIMES:
            logger.warning(f'Retry <{retry_times}> : request of url <{url}>')

        if retry_times > self.spider.settings.RETRY_TIMES:
            logger.error(f'retry {retry_times - 1} times still failed ! \n{e}\n\n')
            pprint(f'retry {retry_times - 1} times still failed ! \n{e}\n\n')
            return

        retry_times += 1

        logger.debug('start request of url <%s>' % url)

        try:
            resp = self.middleware_request(request_instance.request)(config=self.default_config)

        except Exception as e:
            return self._request(request_instance, retry_times, e, resp)

        finally:
            if not resp:
                record_task_info.request_failed_plus()
            else:
                self.task_sender.send_parse(resp)
            # sleep after each request
            time.sleep(self.spider.settings.REQUEST_DELAY)
