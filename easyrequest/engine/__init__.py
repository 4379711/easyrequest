# -*- coding: utf-8 -*-
# @Time    : 2019/11/30 16:29
# @Author  : Liu Yalong
# @File    : __init__.py.py

from concurrent.futures import ThreadPoolExecutor

from easyrequest.middlewares import MixFuncGeneratorMiddleWare
from .register import Register, Listener, Event, record_task_info
from .spider_runner import SpiderRunner


# from easyrequest.utils import split_urls_by_group


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

    def start(self):
        """
        Start manager for listening events .
        """

        # Task sender could send a task to task manager .
        task_sender = Register.task_sender(self.manager)

        # Register a listener to answer the task where the sender send before .
        listener = Listener(self.pool, self.spider_cls, self.spider_data, self.mid_cls, task_sender)

        # Bind a function to deal with events .
        Register.bind_handler(self.manager, Event.EVENT_REQUEST, listener.deal_request_event)
        Register.bind_handler(self.manager, Event.EVENT_PARSE, listener.deal_parse_event)

        # Start event manager .
        self.manager.start()

        # Make sure run() is a generator ,change it to a generator if not .
        request_iter = MixFuncGeneratorMiddleWare(self.spider_cls.from_spider(self.spider_cls).run)()

        # Get all instance of Request from run() .
        for request_instance in request_iter:
            task_sender.send_request(request_instance=request_instance)

        while True:
            request, success, request_failed, parse_failed = record_task_info.info
            if request == (success + request_failed + parse_failed):
                self.stop()
                break

    def stop(self):
        self.manager.stop()

    # def create(self):
    #     """
    #     Multiprocess just used on Linux .
    #     """
    #     if platform.system() == 'Linux' and len(self.spider.start_urls) > 1:
    #
    #         import multiprocessing
    #
    #         urls_iter = split_urls_by_group(self.spider.start_urls, self.setting.PROCESS_NUM)
    #
    #         process_list = []
    #         for urls in urls_iter:
    #             if urls is []:
    #                 break
    #             p = multiprocessing.Process(target=self.create_coroutine, args=(urls,), daemon=True)
    #             p.start()
    #             process_list.append(p)
    #
    #         for i in process_list:
    #             i.join()
    #     else:
    #         self.create_coroutine()
