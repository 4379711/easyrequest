# -*- coding: utf-8 -*-

import time
from easyrequest import Request
from easyrequest.error import ReturnTypeError
from easyrequest.utils.log import logger
from easyrequest.utils.format_print import pprint
from easyrequest.middlewares import MixFuncGeneratorMiddleWare
from easyrequest.utils import RecordTaskInfo

from .event_manage import EventManager

# Record all tasks info .
record_task_info = RecordTaskInfo()


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

        # Flag whether an error occurred .
        error_flag = 0

        func_ = self.middleware_parse.from_spider(self.spider.parse_response)(resp)
        while True:
            try:
                # parse response .
                item = next(func_)
            except StopIteration:
                break
            except Exception as e:
                error_flag = 1
                pprint(f'Parse response failed !\n\t\t {e}\n\n')
                logger.error(f'Parse response failed !\n\t\t {e}\n\n')
                continue
            try:
                # save data .
                logger.debug('Start save data of url <%s>' % url)
                self.data_persistence.save(item)
                record_task_info.save_success_plus()
            except Exception as e:
                pprint(f'Save data failed !\n\t\t {e}\n\n')
                logger.error(f'Save data failed !\n\t\t {e}\n\n')
                record_task_info.save_failed_plus()

        if error_flag == 0:
            record_task_info.parse_success_plus()
        else:
            record_task_info.parse_failed_plus()

    def _request(self, request_instance, retry_times=0, e=None, resp=None):
        assert isinstance(request_instance, Request)

        url = request_instance.url

        if 0 < retry_times <= self.spider.settings.RETRY_TIMES:
            logger.warning(f'Retry <{retry_times}> : request of url <{url}>')

        if retry_times > self.spider.settings.RETRY_TIMES:
            logger.error(f'retry {retry_times - 1} times still failed ! \n{e}\n\n')
            pprint(f'retry {retry_times - 1} times still failed ! \n{e}\n\n')
            record_task_info.request_failed_plus()
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
                record_task_info.request_success_plus()
                self.task_sender.send_parse(resp)
            # sleep after each request
            time.sleep(self.spider.settings.REQUEST_DELAY)


class Event:
    EVENT_REQUEST = "EVENT_REQUEST"
    EVENT_PARSE = "EVENT_PARSE"

    def __init__(self, type_=None):
        self.type_ = type_
        self.event = None


class Listener(SpiderRunner):
    def __init__(self, pool, spider_cls, data_cls, mid_cls_list, task_sender):
        super(Listener, self).__init__(pool, spider_cls, data_cls, mid_cls_list, task_sender)

    def put_request_to_pool(self, request_instance):

        # record task .
        if request_instance.is_filter and record_task_info.is_in_set(request_instance.md5):
            return
        record_task_info.request_add(request_instance.md5)

        # run task .
        self.pool.submit(self._request, request_instance)

    def deal_request_event(self, event):
        request_instance = event.event

        self.put_request_to_pool(request_instance)

    def deal_parse_event(self, event):
        resp = event.event

        if resp.callback is None or resp.callback.__name__ == 'parse_response':
            self._parse_resp_and_save_by_generator(resp)

        else:
            try:
                callback_iter = MixFuncGeneratorMiddleWare(resp.callback)(resp)
                for request_instance in callback_iter:
                    if not isinstance(request_instance, Request):
                        raise ReturnTypeError(Request)
                    self.put_request_to_pool(request_instance)
                record_task_info.parse_success_plus()

            except Exception as e:
                logger.error(f'''Occur Error in <{resp.callback.__name__}>:\n\t{e}''')
                pprint(f'''Occur Error in <{resp.callback.__name__}>:\n\t{e}''')
                record_task_info.parse_failed_plus()
        record_task_info.parse_add(resp.md5)


class SendTasks:
    def __init__(self, event_manager):
        """ Init a event manager ."""
        self.__eventManager = event_manager

    def send_request(self, request_instance):
        """
        Send a instance of Request .
        """

        if not isinstance(request_instance, Request):
            pprint(f'Return Type in all callback function must be an instance of Request ,got {type(request_instance)}')
            logger.error(f'Return Type must be an instance of Request ,got {type(request_instance)}')
            return

        event = Event(type_=Event.EVENT_REQUEST)
        event.event = request_instance
        self.__eventManager.send_event(event)

    def send_parse(self, resp):
        event = Event(type_=Event.EVENT_PARSE)
        event.event = resp
        self.__eventManager.send_event(event)


class Register:
    """
    API for manager , Sender ...
    """

    @staticmethod
    def register_manager():
        # register event manager
        event_manager = EventManager()
        return event_manager

    @staticmethod
    def bind_handler(manager, type_, handler):
        manager.add_event_handler(type_, handler)

    @staticmethod
    def task_sender(manager):
        sender = SendTasks(manager)
        return sender
