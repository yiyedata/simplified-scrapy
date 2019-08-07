#!/usr/bin/python
#coding=utf-8
import logging

class Log(object):
  key = None
  def __init__(self, key):
    if key is not None:
      self.key = key
  def logger(self):
    logger = logging.getLogger(self.key)
    return logging.LoggerAdapter(logger, {'simple-spider': self})

  def log(self, message, level=logging.DEBUG, **kw):
    """Log the given message at the given log level
    This helper wraps a log call to the logger within the spider, but you
    can use it directly (e.g. Spider.logger.info('msg')) or use any other
    Python logger too.
    """
    self.logger().log(level, message, **kw)
    if(level==logging.DEBUG):
      print message