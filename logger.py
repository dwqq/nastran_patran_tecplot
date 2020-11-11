'''
@Description: 
@Author: dwqq
@Date: 2020-03-30 14:34:28
@LastEditTime: 2020-04-27 10:34:08
@LastEditors: dwqq
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from logging import handlers

class Logger(object):
    """Log level relational mapping"""
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(self,filename,level='debug',when='D',backCount=3,fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        """Set the log format and log level"""
        self.logger = logging.getLogger(filename)
        self.logger.handlers.clear()
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str) 
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')
        th.setFormatter(format_str)
        self.logger.addHandler(sh) 
        self.logger.addHandler(th)

if __name__ == '__main__':
    log = Logger('all.log',level='debug')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')
    Logger('error.log', level='error').logger.error('error')