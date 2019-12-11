# -*- coding: utf-8 -*-
# @Time    : 2019/11/30 16:30
# @Author  : Liu Yalong
# @File    : default_settings.py


# write your spider name here which you want to run
SPIDERS = []

# Change user-agent auto
AUTO_USER_AGENT = True

# Configure maximum concurrent requests (default: 10)
CONCURRENT_REQUESTS = 10

# Configure a delay for requests(default: 0)
REQUEST_DELAY = 0

# Disable Console (enabled by default)
CONSOLE_MESSAGE = True

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# SPIDER_MIDDLEWARES = {
#    'aioo.middlewares.AiooSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# DOWNLOADER_MIDDLEWARES = {
#    'aioo.middlewares.AiooDownloaderMiddleware': 543,
# }

# Configure item pipelines
# ITEM_PIPELINES = {
#    'aioo.pipelines.AiooPipeline': 300,
# }