# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 16:09
# @Author  : Liu Yalong
# @File    : log_config.py
import logging
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
import gzip
import os
import time
from easyrequest.utils.singleton import Singleton


class GzTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when, interval, **kwargs):
        super(GzTimedRotatingFileHandler, self).__init__(filename, when, interval, **kwargs)

    def doGzip(self, old_log):
        with open(old_log, 'rb') as old:
            with gzip.open(old_log.replace('.log', '', 1) + '.gz', 'wb') as comp_log:
                comp_log.writelines(old)
        os.remove(old_log)

    # overwrite
    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        if os.path.exists(dfn):
            os.remove(dfn)
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
            self.doGzip(dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


class LogBase(Singleton):

    def __init__(self, dir_path='./logs/',
                 logger_name='special_log_name',
                 info_name='info.log',
                 error_name='error.log',
                 warning_name='warning.log',
                 debug_name='debug.log',
                 interval=7,
                 detail=False,
                 debug=False,
                 info=True,
                 error=True,
                 warning=True,
                 ):

        self.info_name = info_name
        self.error_name = error_name
        self.warning_name = warning_name
        self.debug_name = debug_name
        self.path = dir_path
        self.logger = logging.getLogger(logger_name)
        self.debug = debug
        self.warning = warning
        self.error = error
        self.info = info
        self.detail = detail
        self.interval = interval

    def __handler(self, log_name):
        handler = GzTimedRotatingFileHandler(self.path + log_name,
                                             when='D',
                                             interval=self.interval,
                                             backupCount=3,
                                             encoding='utf-8')
        return handler

    def __filter_message(self, handler, log_level):
        """
        过滤不同等级日志的其他信息,只保留当前日志等级的信息
        :param handler: handler
        :param log_level: 字符串
        :return: handler
        """
        if self.detail:
            formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s",
                                          "%Y%m%d %H:%M:%S")
        else:
            formatter = logging.Formatter("%(asctime)s - %(message)s", "%Y%m%d %H:%M:%S")
        _filter = logging.Filter()

        handler.suffix = "%Y%m%d.log"
        handler.setFormatter(formatter)
        handler.setLevel(log_level)
        _filter.filter = lambda record: record.levelno == log_level
        handler.addFilter(_filter)
        return handler

    def get_logger(self):

        # 添加此行，防止日志重复记录
        if not self.logger.handlers:
            # 设置日志等级,默认是 DEBUG
            self.logger.setLevel(logging.DEBUG)

            levels = [self.debug, self.info, self.warning, self.error]
            log_names = [self.debug_name, self.info_name, self.warning_name, self.error_name]
            levels_ = [10, 20, 30, 40]

            for i, lev in enumerate(levels):
                if lev:
                    _handler = self.__handler(log_names[i])
                    _handler = self.__filter_message(_handler, levels_[i])
                    # handler添加给日志对象
                    self.logger.addHandler(_handler)
        return self.logger

    @staticmethod
    def type_need(parm, type_):
        if not isinstance(parm, type_):
            raise TypeError(f'expect {type_},but got {type(parm)}')
