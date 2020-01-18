# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor

from easyrequest import Request
from easyrequest.middlewares import MixFuncGeneratorMiddleWare
from easyrequest.utils import pprint
from .register import Register, Listener, Event, record_task_info, logger


class SpiderEngine:

    def __init__(self, spider_cls, spider_data, mid_cls):
        """
        This is a engine for scheduling all modules .

        :param spider_cls: Class of spider written by user .
        :param spider_data: Class of save data written by user .
        :param mid_cls: Class of middleware written by user .
        """
        self.spider_cls = spider_cls
        self.setting = spider_cls.settings
        self.spider_data = spider_data
        self.mid_cls = mid_cls
        # Create a thread pool for requesting urls .
        self.pool = ThreadPoolExecutor(max_workers=self.setting.CONCURRENT_REQUESTS)
        # Create a event manager .
        self.manager = Register.register_manager()
        self.task_sender = None

    def register_modules(self):
        """
         Register manager for listening events, bind handler, task sender .
        """

        # Task sender could send a task to task manager .
        self.task_sender = Register.task_sender(self.manager)

        # Register a listener to answer the task where the sender send before .
        listener = Listener(self.pool, self.spider_cls, self.spider_data, self.mid_cls, self.task_sender)

        # Bind a function to deal with events .
        Register.bind_handler(self.manager, Event.EVENT_REQUEST, listener.deal_request_event)
        Register.bind_handler(self.manager, Event.EVENT_PARSE, listener.deal_parse_event)

        # Start event manager .
        self.manager.start()

    def start(self):
        """
        Start engine .
        """

        self.register_modules()

        # Make sure run() is a generator ,change it to a generator if not .
        request_iter = MixFuncGeneratorMiddleWare(self.spider_cls.from_spider(self.spider_cls).run)()

        # Get all instance of Request from run() .
        for request_instance in request_iter:
            if not isinstance(request_instance, Request):
                pprint(f'Return Type in run() must be an instance of Request ,got {type(request_instance)}')
                logger.error(f'Return Type in run() must be an instance of Request ,got {type(request_instance)}')
                self.stop()
                return
            self.task_sender.send_request(request_instance=request_instance)

        while True:
            request_success, request_failed, parse_success, parse_failed, save_success, save_failed = \
                record_task_info.info

            if request_success == (parse_success + parse_failed) != 0 and \
                    record_task_info.requests_is_empty:
                info_str = f"""The result of this task:
                
                Request successful : {request_success} 
                Request failed     : {request_failed} 
                Parse successful   : {parse_success} 
                Parse failed       : {parse_failed} 
                Save successful    : {save_success} 
                Save failed        : {save_failed} 

                """
                logger.info(info_str)
                self.stop()
                break

    def stop(self):
        self.manager.stop()
