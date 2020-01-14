# -*- coding: utf-8 -*-
# @Time    : 2019/11/30 16:29
# @Author  : Liu Yalong
# @File    : __init__.py.py

import platform

from easyrequest.middlewares import MixFuncGeneratorMiddleWare
from easyrequest.utils import split_urls_by_group
from .register import Register, Listener, Event
from .spider_runner import SpiderRunner
from gevent.pool import Pool
from gevent import monkey

monkey.patch_socket()


class SpiderEngine:
    """
    Scheduling all modules .
    """

    def __init__(self, spider_cls, spider_data, mid_cls):
        self.spider_cls = spider_cls
        self.setting = spider_cls.settings
        self.spider_data = spider_data
        self.mid_cls = mid_cls
        self.pool = Pool(size=self.setting.CONCURRENT_REQUESTS)

    def start(self):
        """
        Start manager for listening events .
        """
        manager = Register.register_manager()
        task_sender = Register.task_sender(manager)

        listener = Listener(self.pool, self.spider_cls, self.spider_data, self.mid_cls, task_sender)

        Register.bind_handler(manager, Event.EVENT_REQUEST, listener.deal_request_event)
        Register.bind_handler(manager, Event.EVENT_PARSE, listener.deal_parse_event)
        manager.start()

        print('即将开始请求!')
        request_iter = MixFuncGeneratorMiddleWare(self.spider_cls.from_spider(self.spider_cls).run)()

        for request_instance in request_iter:
            task_sender.send_request(request_instance=request_instance)

        # self.pool.join()

    # def create(self):
    #     """
    #     Multiprocess just used in Linux .
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
