# -*- coding: utf-8 -*-
# @Time    : 2019/11/30 16:29
# @Author  : Liu Yalong
# @File    : __init__.py.py

import platform
from easyrequest.entrance.spider_runner import SpiderRunner
from easyrequest.utils import split_urls_by_group
import gevent
from gevent.pool import Pool
from gevent import monkey

monkey.patch_socket()


class SpiderEngine:
    def __init__(self, spider, spider_data, mid_cls):
        self.spider = spider
        self.setting = spider.settings
        self.spider_data = spider_data
        self.mid_cls = mid_cls

    def load_config(self):
        setting = self.spider.settings
        return setting

    def create_coroutine(self, urls):
        pool = Pool(size=self.setting.CONCURRENT_REQUESTS)
        runner = SpiderRunner(self.spider, self.spider_data, self.mid_cls)
        gevent.joinall([pool.spawn(runner.start, url) for url in urls])

    def create(self):
        if platform.system() == 'Linux':

            import multiprocessing

            urls_iter = split_urls_by_group(self.spider.start_urls, self.setting.PROCESS_NUM)

            process_list = []
            for urls in urls_iter:
                if urls is []:
                    break
                p = multiprocessing.Process(target=self.create_coroutine, args=(urls,), daemon=True)
                p.start()
                process_list.append(p)

            for i in process_list:
                i.join()
        else:
            self.create_coroutine(self.spider.start_urls)
