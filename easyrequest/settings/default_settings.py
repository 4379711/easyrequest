# -*- coding: utf-8 -*-

# Configure maximum concurrent requests (default: 10)
CONCURRENT_REQUESTS = 10

# Record the pid in file for killing it .(default: False)
RECORD_PID = False

# Timeout of per request (default:300 seconds)
DEFAULT_REQUEST_TIMEOUT = 300

# Either a boolean, in which case it controls whether we verify the server's TLS certificate
# OR a string, in which case it must be a path to a CA bundle to use.
DEFAULT_REQUEST_VERIFY = False

# Configure a delay seconds for requests(default: 0)
REQUEST_DELAY = 0

# Retry times per request when it failed
RETRY_TIMES = 3

# Default request headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# Configure log
# LOG_PATH : Path(relative path) where to save
# DEBUG    : Whether open DEBUG MODE
# INTERVAL : How often unpack logs
LOG_CONFIG = {
    'LOG_PATH': 'logs',
    'DEBUG': True,
    'INFO': True,
    'WARNING': True,
    'ERROR': True,
    'INTERVAL': 7
}

# TIMER TASK config
TIMER_TASK = [
    {'SpiderName': '',
     'every': 1,
     'unit': 'days.at("10:00")',  # <at> can not use in ( seconds ,minutes ,hour...)
     # 'unit': 'seconds'
     },
]
