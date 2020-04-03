#!/usr/bin/python
#coding=utf-8
# import json,random,sqlite3,logging,os
# import sys
# from simplified_scrapy.core.utils import printInfo,getTimeNow,md5
  
class UrlStoreBase():

  def popUrl(self):
    raise NotImplementedError

  def getCount(self):
    raise NotImplementedError

  def checkUrl(self,url):
    raise NotImplementedError

  def saveUrl(self, urls,i=None):
    raise NotImplementedError

  def clearUrl(self):
    pass
  def resetUrls(self, urls):
    raise NotImplementedError
  def updateState(self, url, state):
    raise NotImplementedError