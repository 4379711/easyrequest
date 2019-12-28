# -*- coding: utf-8 -*-
# @Time    : 2019/10/22 13:33
# @Author  : Liu Yalong
# @File    : __init__.py
from .log_config import LogBase
import os

__all__ = ['MyLog']


class MyLog(LogBase):
    """
    功能:
        将日志分日志等级记录,并自动压缩2019-11-11.info.log.gz

    参数:
        :param dir_path: 日志记录的路径,默认是当前路径下的log文件夹
        :param logger_name: logger对象的名字
        :param info_name: 保存info等级的文件名字
        :param error_name:
        :param warning_name:
        :param debug_name:
        :param interval: 压缩日志的频率,默认是7天
        :param detail: bool值,记录日志是否为详细记录
        :param debug: 是否记录debug,默认不记录
        :param info: 是否记录info,默认记录
        :param error:
        :param warning:
    实例方法:
        get_logger()-->logger

    使用举例:
        # 记录四种类型的日志
        logger = MyLog(debug=True).get_logger()
        logger.info('info')
        logger.debug('debug')
        logger.error('error')
        logger.warning('warning')

        # # # # # # # # # # # # # # # # # # # # # # # # #

        # 只记录错误日志
        logger = MyLog(info=False,warning=False).get_logger()
        logger.info('info')
        logger.debug('debug')
        logger.error('error')
        logger.warning('warning')
    注意:
        MyLog()的实例只会同时存在一个,默认记录首次创建实例的属性.
        例如:

            mylog = MyLog('./logs/logs/')
            mylog2 = MyLog()
            logger = mylog.get_logger()
            logger2 = mylog2.get_logger()
            logger.info('info')

            logger2 = MyLog('./logs/logs2/').get_logger()
            logger2.info('info2')

            以上两个logger logger2,会以logger(第一次创建实例)的属性为准,日志会存放在./logs/logs/下



    """

    def __init__(self, log_path: str = './logs/', **kwargs):
        self.type_need(log_path, str)
        if not log_path.endswith('/'):
            log_path += '/'
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        super(MyLog, self).__init__(dir_path=log_path, **kwargs)
