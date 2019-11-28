#!/usr/bin/python
#coding=utf-8
import os,io,json
import sys
from simplified_scrapy.core.dictex import Dict
if sys.version_info.major == 2:
  from urlparse import urlparse
else:
  import urllib
  urlparse = urllib.parse.urlparse
class MemCookieStore:
  _cookies=Dict()
  
  def __init__(self):
    pass

  def getCookie(self, url):
    domain = urlparse(url).netloc
    cookie = self._getCookie(domain)
    if(not cookie):
      start = domain.index('.')+1
      domain = domain[start:]
      cookie = self._getCookie(domain)
    return cookie

  def _getCookie(self, domain):
    cookie = self._cookies.get(domain)
    return cookie

  def setCookie(self, url, cookie):
    if(not cookie): return
    domain = urlparse(url).netloc
    kvs={}
    old = self._getCookie(domain)
    if(old):
      self._parseCookie(old,kvs)

    if(isinstance(cookie,str)):
      self._parseCookie(cookie,kvs)
    else:
      for line in cookie:
        self._parseCookie(line,kvs)
    strCookie = self._dic2str(kvs)
    self._cookies[domain] = strCookie
  def _dic2str(self, dic):
    strs=None
    for k,v in dic.items():
      if(strs):
        strs = u'{};{}={}'.format(strs,k,v)
      else:
        strs = u'{}={}'.format(k,v)
    return strs

  def _parseCookie(self, cookie, kvs):
    keys = cookie.split(';')
    for key in keys:
      if(not key): continue
      key = key.strip()
      kv = key.split('=')
      name = kv[0].strip().lower()
      flag=False
      for kp in ['expires','domain','path','secure','httponly']:
        if(name == kp):
          flag=True
          break
      if(flag): continue
      value=''
      if(len(kv)>1): value=kv[1].strip()
      kvs[kv[0].strip()]=value
    
