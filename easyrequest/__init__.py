# -*- coding: utf-8 -*-
# @Time    : 2019/11/28 15:41
# @Author  : Liu Yalong
# @File    : __init__.py.py


import sys

# Check required Python version
if sys.version_info < (3, 6):
    print("\033[32mError: EasyRequest requires Python 3.6+\033[0m")
    sys.exit(1)
del sys

from easyrequest import schedule
from easyrequest.items import Items
from easyrequest.request.request import Request
from easyrequest.request.spider import CrawlSpider
from easyrequest.request.parse_response import Parser
from easyrequest.utils.log import logger
from easyrequest.entrance.run_spider_by_manage import *
