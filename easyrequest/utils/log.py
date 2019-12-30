# -*- coding: utf-8 -*-
# @Time    : 2019/12/28 13:44
# @Author  : Liu Yalong
# @File    : log.py

from easyrequest.utils.load_module import load_module_from_path
import os
from os.path import join
import sys
from easyrequest.settings.load_settings import overridden_settings
from easyrequest.logs import MyLog

cmd_path = os.getcwd()
sys.path.insert(0, cmd_path)

try:
    # load user config
    user_settings_obj = load_module_from_path('settings.py', join(cmd_path, 'settings.py'))
    # override default config
    settings = overridden_settings(user_settings_obj)
    config_dict = settings.LOG_CONFIG

    _LOG = MyLog(
        log_path=join(cmd_path, config_dict.get('LOG_PATH', 'logs')),
        interval=config_dict.get('INTERVAL', 7),
        debug=config_dict.get('DEBUG', False),
        info=config_dict.get('INFO', False),
        error=config_dict.get('ERROR', True),
        warning=config_dict.get('WARNING', False)
    )
    logger = _LOG.get_logger()
except FileNotFoundError:
    logger = None
