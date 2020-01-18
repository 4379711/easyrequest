# -*- coding: utf-8 -*-

from easyrequest.engine import SpiderEngine
from easyrequest.engine.load_all_modules import LoadAllModules
from easyrequest.error import LoadError
from easyrequest.utils import *


def start_spider(spider_name):
    """
    Run a spider .
    """
    if not check_spider_name(spider_name):
        return
    if not check_project_file(spider_name):
        return

    # load all module for project
    all_module = LoadAllModules(spider_name)
    settings = all_module.load_user_config()
    spider_cls_list = all_module.load_spider_cls()
    spider_data_cls = all_module.load_data_persistence_cls()
    spider_middleware_cls_list = all_module.load_middleware_cls()

    if not spider_cls_list or not spider_data_cls or not spider_middleware_cls_list:
        raise LoadError(spider_name)

    if settings.RECORD_PID:
        # record process pid in file
        write_process_pid(spider_name)

    # Only load last spider
    spider_cls = spider_cls_list.pop()
    spider_data_cls = spider_data_cls.pop()

    # set spider config
    spider_cls.settings = settings
    spider_cls.spider_name = spider_name

    # create engine
    engine = SpiderEngine(spider_cls, spider_data_cls, spider_middleware_cls_list)
    engine.start()

