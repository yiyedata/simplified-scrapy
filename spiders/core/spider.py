#!/usr/bin/python
#coding=utf-8
import json,re,logging,time,io,os,hashlib
from log import Log
from url_store import UrlStore
class Spider(Log):
  name = None
  models = None
  concurrencyPer1s=0.5
  htmlPath='htmls/'
  def __init__(self, name=None):
    if name is not None:
      self.name = name
    elif not getattr(self, 'name', None):
      raise ValueError("%s must have a name" % type(self).__name__)
    if not hasattr(self, 'start_urls'):
      self.start_urls = []
    if not hasattr(self, 'url_store'):
      print 'init url_store------------------------'
      self.url_store = UrlStore()
    Log.__init__(self,self.name)
    self.url_store.saveUrl(self.start_urls)

  def beforeRequest(self, request):
    # request['proxy']=random.choice(spider_resource.proxyips)
    # self.log(request)
    return request

  def _getResponseStr(self, htmSource,url):
    html=None
    try:
      html=htmSource.decode("utf8")
    except: #Exception as e:
      try:
        html=htmSource.decode("gbk")
      except Exception as err:
        self.log('{},{}'.format(err,url),logging.ERROR)
    return html
  def afterResponse(self, response, cookie, url):
    html = self._getResponseStr(response.read(),url)
    data = {
      "html" : html,
      "header" : response.info().headers,
      "cookie" : cookie,
      "url" : url
    }
    self.saveHtml(url,html)
    return html
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
    # print data
    if(data):
      objs = json.loads(data)
      for obj in objs:
        if(obj.get("Urls")):
          self.saveUrl(obj)
        else:
          self.saveObj(obj)

  def saveHtml(self,url,html):
    filename = os.path.basename(url)
    if(not filename):
      filename = hashlib.md5(url).hexdigest()+'.htm'
    if(not os.path.exists(self.htmlPath)):
      os.mkdir(self.htmlPath)
    file = io.open(self.htmlPath+filename, "w",encoding="utf-8")
    file.write(html)
    file.close()

  def saveObj(self, data):
    # print data
    raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))

  _downloadPageNum=0
  _startCountTs=time.time()
  def checkConcurrency(self):
    tmSpan = time.time()-self._startCountTs
    if(tmSpan>10):
      if(self._downloadPageNum>(self.concurrencyPer1s*tmSpan)):
        return False
      self._startCountTs=time.time()
      self._downloadPageNum=1
    else:
      self._downloadPageNum=self._downloadPageNum+1
    return True
  def getUrl(self):
    if(self.checkConcurrency()):
      return self.url_store.getUrl()
    return None

  def saveUrl(self, urls):
    self.url_store.saveUrl(urls)

