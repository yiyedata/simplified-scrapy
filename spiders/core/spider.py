#!/usr/bin/python
#coding=utf-8
import json,re,logging,time,io,os,hashlib
from log import Log
from url_store import UrlStore
from html_store import HtmlStore
from obj_store import ObjStore
from cookie_store import CookieStore
from request_helper import requestPost,requestGet,getResponseStr,extractHtml
class Spider(Log):
  name = None
  models = None
  concurrencyPer1s=1
  def __init__(self, name=None):
    if name is not None:
      self.name = name
    elif not getattr(self, 'name', None):
      raise ValueError("%s must have a name" % type(self).__name__)
    if not hasattr(self, 'start_urls'):
      self.start_urls = []
    if not hasattr(self, 'url_store'):
      print 'init url_store------------------------'
      self.url_store = UrlStore(self.name)
    if not hasattr(self, 'html_store'):
      print 'init html_store------------------------'
      self.html_store = HtmlStore()
    if not hasattr(self, "obj_store"):
      print 'init obj_store------------------------'
      self.obj_store = ObjStore()
    if not hasattr(self, "cookie_store"):
      print 'init cookie_store------------------------'
      self.cookie_store = CookieStore()
    if not hasattr(self, "login_data"):
      self.login_data = None

    Log.__init__(self,self.name)
    self.url_store.saveUrl(self.start_urls)
  def login(self, obj=None):
    if(not obj): obj = self.login_data
    if(obj and obj.get('url')):
      data = obj.get('data')
      if(data and not isinstance(data,str)): data = json.dumps(data)
      if(obj.get('method')=='get'):
        return requestGet(obj.get('url'),obj.get('headers'),obj.get('useProxy'),self)
      else:
        return requestPost(obj.get('url'),data,
          obj.get('headers'),obj.get('useProxy'),self)
    else:
      return True
  def getCookie(self,url):
    if(self.cookie_store):
      return self.cookie_store.getCookie(url)
    return None
  def setCookie(self,url,cookie):
    if(self.cookie_store and cookie):#cookie 拼接，不同页面返回不同的cookie，不能覆盖
      self.cookie_store.setCookie(url,cookie)

  def beforeRequest(self, request):
    cookie=self.getCookie(request['url'])
    if(cookie):
      request['header']['Cookie']=cookie
    return request

  def afterResponse(self, response, url):
    html = getResponseStr(response.read(),url)
    cookie = response.info().getheaders('Set-Cookie')
    self.setCookie(url,cookie)
    return html

  def popHtml(self):
    return self.html_store.popHtml()
  def saveHtml(self,url,html):
    if(html):
      self.html_store.saveHtml(url,html)
  def updateHtmlState(self,url,state):
    self.html_store.updateState(url,state)
    
  def removeScripts(self,html):
    html = re.compile('(?=<[\s]*script[^>]*>)[\s\S]*?(?:</script>)').sub('',html)
    html = re.compile('(?=<[\s]*style[^>]*>)[\s\S]*?(?:</style>)').sub('',html)
    html = re.compile('(?=<!--)[\s\S]*?(?:-->)').sub('',html)
    html = re.compile('(?=<[\s]*link )[\s\S]*?(?:>)').sub('',html)
    html = re.compile('(?=<[\s]*meta )[\s\S]*?(?:>)').sub('',html)
    html = re.compile('(?=<[\s]*object[^>]*>)[\s\S]*?(?:</object>)').sub('',html)
    html = re.compile('</object>').sub('',html)
    html = re.compile('(?=<param )[\s\S]*?(?:/>)').sub('',html)
    return html
  def downloadError(self,url,err=None):
    print url,err

  def saveData(self, data):
    if(data):
      if(type(data).__name__ == 'dict'): objs = data
      else: objs = json.loads(data)
      for obj in objs:
        if(obj.get("Urls")):
          self.saveUrl(obj.get("Urls"))
        else:
          d = obj.get("Data")
          if(d and len(d) > 0):
            self.obj_store.saveObj(d[0])

  def extract(self, url,html,models,modelNames):
    if(not modelNames):
      print 'model not configured'
      return False
    else:
      return extractHtml(url["url"],html,models,modelNames,url.get("title"))

  _downloadPageNum=0
  _startCountTs=time.time()
  def checkConcurrency(self):
    tmSpan = time.time()-self._startCountTs
    if(tmSpan>10):
      if(self._downloadPageNum>(self.concurrencyPer1s*tmSpan)):
        return False
      self._startCountTs=time.time()
      self._downloadPageNum=1
    elif self.url_store.getCount()>0:
      self._downloadPageNum=self._downloadPageNum+1
    return True
  def popUrl(self):
    if(self.checkConcurrency()):
      return self.url_store.popUrl()
    else:
      print 'Downloads are too frequent'
    return None
  def urlCount(self):
    return self.url_store.getCount()
  def saveUrl(self, urls):
    self.url_store.saveUrl(urls)

