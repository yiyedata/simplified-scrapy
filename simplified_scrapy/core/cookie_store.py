#!/usr/bin/python
#coding=utf-8
import os,io,json
import sys
from simplified_scrapy.core.utils import printInfo
if sys.version_info.major == 2:
  from urlparse import urlparse
else:
  import urllib
  urlparse = urllib.parse.urlparse
class CookieStore:
  _cookies={}
  _cookieFilename = 'db/cookies.yd'
  
  def __init__(self):
    try:
      if(not os.path.exists('db/')):
        os.mkdir('db/')
      self._cookiefile = io.open(self._cookieFilename, "a+",encoding="utf-8")
      self._cookiefile.seek(0)
      line = 'start'
      while(line):
        line = self._cookiefile.readline()
        if(line):
          line=line[:-1]
          start=line.index(',')
          if(start>0):
            self._cookies[line[0:start]]=line[start+1:]
      self._refreshCookieFile()
    except Exception as err:
      printInfo(err) 
  def _refreshCookieFile(self):
    self._cookiefile.seek(0)
    self._cookiefile.truncate()
    for k,v in self._cookies.items():
      self._cookiefile.write(u'{},{}\n'.format(k,v))
      
    self._cookiefile.flush()

  def __del__(self):
    self._cookiefile.close()

  def getCookie(self, url):
    domain = urlparse(url).netloc
    cookie = self._cookies.get(domain)
    if(not cookie):
      start = domain.index('.')+1
      domain = domain[start:]
      cookie = self._cookies.get(domain)
    return cookie
  def setCookie(self, url, cookie):
    if(not cookie): return
    domain = urlparse(url).netloc
    kvs={}
    old=self._cookies.get(domain)
    if(old):
      self._parseCookie(old,kvs)

    if(not isinstance(cookie,list)):
      self._parseCookie(cookie,kvs)
    else:
      for line in cookie:
        self._parseCookie(line,kvs)
    strCookie = self._dic2str(kvs)
    self._cookies[domain] = strCookie
    self._cookiefile.write(u'{},{}\n'.format(domain,strCookie))
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
    

# tmp = CookieStore()
# tmp.setCookie('http://127.0.0.1:1001/demo','sid=s%3A1s-KtykINQomDW5-5iduk6BOkX1tCT96.9qTyuzOf7Ds6nfNkQhP8PVMZ3qbpukqmX5multsqdbQ; Path=/; HttpOnly')
