#!/usr/bin/python
#coding=utf-8
import simplified_scrapy.core.logex
from simplified_scrapy.core.request_helper import requestGet as _get,requestPost as _post
from simplified_scrapy.spider import Spider
from simplified_scrapy.core.mem_cookiestore import MemCookieStore as _store

class _MemSpider(Spider):
  def __init__(self, name=None):
    self.cookie_store = _store()

class _Request():
  def __init__(self):
    self._ssp_ = _MemSpider()
  def get(self,url,header=None,timeout=30,useIp=False,saveCookie=True):
    ssp = None
    if(saveCookie): ssp=self._ssp_
    return _get(url,header,useIp,ssp,timeout,True)

  def post(self,url,data=None,header=None,timeout=30,useIp=False,saveCookie=True):
    ssp = None
    if(saveCookie): ssp=self._ssp_
    return _post(url,data,header,useIp,ssp,timeout,True)
  def getCookie(self,url):
    return self._ssp_.getCookie(url)
  def setCookie(self,url,cookie):
    self._ssp_.setCookie(url,cookie)
  def setCookieStore(self,cookieStore):
    self._ssp_.cookie_store = cookieStore
req = _Request()