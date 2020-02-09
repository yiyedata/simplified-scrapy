#!/usr/bin/python
#coding=utf-8
import json,re,logging,time,io,os
import sys
from simplified_scrapy.core.config_helper import Configs
from simplified_scrapy.core.sqlite_cookiestore import SqliteCookieStore
from simplified_scrapy.core.request_helper import requestPost,requestGet,getResponseStr,extractHtml
from simplified_scrapy.core.utils import convertTime2Str,convertStr2Time,printInfo,absoluteUrl
from simplified_scrapy.core.regex_helper import *
from simplified_scrapy.core.sqlite_urlstore import SqliteUrlStore
from simplified_scrapy.core.sqlite_htmlstore import SqliteHtmlStore
from simplified_scrapy.core.obj_store import ObjStore

class Spider():
  name = None
  models = None
  concurrencyPer1s=1
  use_cookie = True
  use_ip = False # globle
  version = "0.0.1"
  request_timeout = None
  allowed_domains = []
  excepted_domains = []
  custom_down = False # globle
  useragent = None
  proxyips = None
  logged_in = False
  login_data = None
  refresh_urls = False
  stop = False
  encodings = {}
  def __init__(self, name=None):
    try:
      if name is not None:
        self.name = name
      elif not getattr(self, 'name', None):
        raise ValueError("%s must have a name" % type(self).__name__)
      if not hasattr(self, 'start_urls'):
        self.start_urls = []
      if not hasattr(self, 'url_store'):
        # printInfo('init url_store------------------------')
        self.url_store = SqliteUrlStore(self.name)
      if not hasattr(self, 'html_store'):
        # printInfo('init html_store------------------------')
        self.html_store = SqliteHtmlStore(self.name)
      if not hasattr(self, "obj_store"):
        # printInfo('init obj_store------------------------')
        self.obj_store = ObjStore(self.name)
      if not hasattr(self, "cookie_store"):
        # printInfo('init cookie_store------------------------')
        self.cookie_store = SqliteCookieStore()
      if not self.refresh_urls:
        self.url_store.saveUrl(self.start_urls,0)
      else:
        self.url_store.resetUrls(self.start_urls)
      self.listA=listA
      self.listImg=listImg
      self.getElementsByTag=getElementsByTag
      self.getElementByID=getElementByID
      self.getElementsByClass=getElementsByClass
      self.getElementByTag=getElementByTag
      self.getElementByClass=getElementByClass
      self.getElement=getElement
      self.getElements=getElements
      self.getElementByAttr=getElementByAttr
      self.getParent=getParent
      self.getChildren=getChildren
      self.getNexts=getNexts
      self.getSection=getSection
      self.removeHtml=removeHtml
      self.trimHtml=trimHtml
      self.removeScripts=removeScripts
      self.tm=0
      self.absoluteUrl=absoluteUrl
    except Exception as err:
      self.log(err,logging.ERROR)

  def log(self, msg, level=logging.DEBUG):
    printInfo(msg)
    logger = logging.getLogger()
    logging.LoggerAdapter(logger, None).log(level, msg)
    
  def login(self, obj=None):
    if(not obj): obj = self.login_data
    if(obj and obj.get('url')):
      data = obj.get('data')
      # if(data and isinstance(data,dict)): 
      #   data = json.dumps(data)
      if(obj.get('method')=='get'):
        return requestGet(obj.get('url'),obj.get('headers'),obj.get('useProxy'),self)
      else:
        return requestPost(obj.get('url'),data,
          obj.get('headers'),obj.get('useProxy'),self)
    else:
      return False
  def getCookie(self,url):
    if(self.use_cookie and self.cookie_store):
      return self.cookie_store.getCookie(url)
    return None
  def setCookie(self,url,cookie):
    if(self.use_cookie and self.cookie_store and cookie):
      self.cookie_store.setCookie(url,cookie)

  def beforeRequest(self, url, request):
    cookie = self.getCookie(url)
    if(cookie):
      if sys.version_info.major == 2:
        request.add_header('Cookie', cookie)
      else:
        request.add_header('Cookie', cookie)
    return request

  def afterResponse(self, response, url,error=False):
    html = getResponseStr(response, url,self,error)
    if sys.version_info.major == 2:
      cookie = response.info().getheaders('Set-Cookie')
    else:
      cookie = response.info().get('Set-Cookie')
    self.setCookie(url,cookie)
    return html
  def renderUrl(self, url, callback):
    printInfo('Need to implement method "renderUrl"')
  def customDown(self, url):
    printInfo('Need to implement method "customDown"')
  def popHtml(self,state=0):
    return self.html_store.popHtml(state)
  def saveHtml(self,url,html):
    if(html):
      self.html_store.saveHtml(url,html)
  def updateHtmlState(self,id,state):
    self.html_store.updateState(id,state)
    
  def downloadError(self,url,err=None):
    printInfo('error url:',url,err)
    self.url_store.updateState(url,2)

  def isPageUrl(self, url):
    if(not url): 
      return False
    if("html.htm.jsp.asp.php".find(url[-4:].lower())>=0):
      return True
    
    if('.jpg.png.gif.bmp.rar.zip.pdf.doc.xls.ppt.exe.avi.mp4'.find(url[-4:].lower())>=0
        or '.jpeg.xlsx.pptx.docx'.find(url[-5:].lower())>=0 
        or '.rm'.find(url[-3:].lower())>=0):
      return False
    return True

  def urlFilter(self, url):
    if(self.excepted_domains):
      for d in self.excepted_domains:
        if(url.find(d)>-1): return False
    if(self.allowed_domains):
      for d in self.allowed_domains:
        if(url.find(d)>-1): return True
      return False
    return True
  def _urlFilter(self, urls):
    tmp=[]
    for url in urls:
      u = url['url']
      if u and self.urlFilter(u):
        tmp.append(url)
    return tmp

  def saveData(self, data):
    if(data):
      if(not isinstance(data,list) and not isinstance(data,dict)): objs = json.loads(data)
      elif isinstance(data,dict):
        objs = [data]
      else: objs = data
      for obj in objs:
        if(obj.get("Urls")):
          self.saveUrl(obj.get("Urls"))
        ds = obj.get("Data")
        if(ds and len(ds) > 0):
          for d in ds:
            self.saveObj(d)
            # self.obj_store.saveObj(d)
  def saveObj(self,data):
    self.obj_store.saveObj(data)

  def extract(self, url,html,models,modelNames):
    if(not modelNames):
      # printInfo('model not configured')
      return False
    else:
      return extractHtml(url["url"],html,models,modelNames,url.get("title"))

  _downloadPageNum=0
  _startCountTs=time.time()
  def checkConcurrency(self):
    tmSpan = time.time()-self._startCountTs
    if(self._downloadPageNum>(self.concurrencyPer1s*tmSpan)):
      return False
    self._startCountTs=time.time()
    self._downloadPageNum=0
    return True
  def popUrl(self):
    if(self.checkConcurrency()):
      url = self.url_store.popUrl()
      if url: self._downloadPageNum=self._downloadPageNum+1
      return url
    else:
      printInfo('Downloads are too frequent')
    return None
  def urlCount(self):
    return self.url_store.getCount()
  def saveUrl(self, urls):
    if not isinstance(urls,list): urls=[urls]
    urls=self._urlFilter(urls)
    self.url_store.saveUrl(urls)

  def plan(self):
    return []

  def resetUrlsTest(self):
    self.url_store.resetUrls(self.start_urls)
  def resetUrls(self,plan):
    if(plan and len(plan)>0):
      for p in plan:
        now = time.localtime()
        hour = now[3]
        minute = now[4]
        if(p.get('hour')):
          hour = p.get('hour')
        if(p.get('minute')):
          minute = p.get('minute')
        planTime = time.strptime(u"{}-{}-{} {}:{}:00".format(now[0],now[1],now[2],hour,minute), "%Y-%m-%d %H:%M:%S")
        configKey = u"plan_{}".format(self.name)
        _lastResetTime=Configs.getValue(configKey)
        if(now > planTime and (not _lastResetTime or convertStr2Time(_lastResetTime)<planTime)):
          self.url_store.resetUrls(self.start_urls)
          Configs.setValue(configKey, convertTime2Str(planTime))
          return


    
