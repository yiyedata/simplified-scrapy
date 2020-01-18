#!/usr/bin/python
#coding=utf-8
import logging
import simplified_scrapy.core.logex
import threading,traceback,time,importlib,imp,os,json,io
from imp import reload
from simplified_scrapy.dictex import Dict
from concurrent.futures import ThreadPoolExecutor
from simplified_scrapy.core.utils import printInfo,getFileModifyTime,isExistsFile
from simplified_scrapy.downloader import execDownload
from simplified_scrapy.extracter import Extracter
import sys
if sys.version_info.major == 2:
  reload(sys)
  sys.setdefaultencoding('utf-8')
try:
  from setting import SETTINGFILE
except ImportError:
  SETTINGFILE = 'setting.json'
class _SimplifiedMain():
  def __init__(self):
    try:
      self.downloadCount=0
      self._runflag = True
      self._settingObj = Dict()
      self.singleSSP = None
      self._extracter = None
      self._pool = None
    except Exception as err:
      self.log(err,logging.ERROR)
  
  def _init(self,ssp=None):
    try:
      self.singleSSP = ssp
      self.refrashSSP()
      self._extracter = Extracter()
      self._pool = ThreadPoolExecutor(max_workers=self._settingObj["max_workers"])
    except Exception as err:
      self.log(err,logging.ERROR)

  def refrashSSP(self):
    try:
      if(os.path.exists(SETTINGFILE)):
        settingJson = io.open(SETTINGFILE, "r",encoding="utf-8").read()
        settingObj = json.loads(settingJson)
        dicTmp = []
        if(not self.singleSSP and settingObj.get('spiders')):
          for spider in settingObj['spiders']:
            try:
              if not spider.get('stop'):
                dicTmp.append(spider['file'])
                self.getSpider(spider['file'],spider["class"])
            except Exception as err:
              self.log(err,logging.ERROR)

          keys = self._spiderDic.keys()
          for key in keys:
            if(key not in dicTmp):
              del self._spiderDic[key]
      else:
        settingObj = Dict()
      if(self.singleSSP): 
        if not self.singleSSP.logged_in: 
          self.singleSSP.logged_in = self.singleSSP.login()
        self._spiderDic[self.singleSSP.name] = self.singleSSP

      if(not settingObj.get("concurrency")):
        settingObj["concurrency"] = 5
      if(not settingObj.get("concurrencyPer1S")):
        settingObj["concurrencyPer1S"] = 10
      if(not settingObj.get("intervalTime")):
        settingObj["intervalTime"] = 0.3
      if(not settingObj.get("max_workers")):
        settingObj["max_workers"] = 10
      if(not settingObj.get("refresh_tm")):
        settingObj["refresh_tm"] = 60
      if(not settingObj.get("disable_extract")):
        settingObj["disable_extract"] = False
      
      self._settingObj = settingObj
    except Exception as err:
      self.log(err,logging.ERROR)
    
  def log(self, msg, level=logging.DEBUG):
    if (isinstance(msg,UnicodeEncodeError)):
      printInfo('UnicodeEncodeError', msg)
      return
    printInfo(msg)
    if(level==logging.ERROR):
      logger = logging.getLogger()
      logging.LoggerAdapter(logger, None).log(level, msg)

  def setRunFlag(self, flag):
    self._runflag = flag

  _started=False
  _spiderDic = Dict()
  def startThread(self,ssp=None):
    if(self._started): return
    self._started = True

    self._init(ssp)
    if(not self._settingObj["disable_extract"]):
      threadExtract = threading.Thread(target=self.extractThread)
      threadExtract.start()
    else:
      self.log('extract disabled......')
    startTime = time.time()
    self.log('simplified-scrapy is running......')
    while self._runflag:
      if((time.time()-startTime) > self._settingObj["refresh_tm"]):
        startTime = time.time()
        self.refrashSSP()
      try:
        if(os.path.exists('stop.txt')):
          self._runflag = False
          os.rename('stop.txt','stoped.txt')
          break
        urlFlag = False
        for ssp in self._spiderDic.values():
          if(not ssp or ssp.stop): continue
          urlCount = ssp.urlCount()
          if(self.checkConcurrency(ssp.name,urlCount)):
            url = ssp.popUrl()
            if(url):
              link = url.get('url')
              if(not link):
                link = url.get('href')
              if(not link):
                link = url.get('src')
              if(not link): raise Exception('no url parameter')
              url['url']=link

              urlFlag = True
              self.downloadCount+=1
              if(isinstance(url,dict) and url.get("requestMethod")=="render"):
                self.downloadRender(url,ssp)
              else:
                self._pool.submit(self.downloadThread2,url,ssp)
            else:
              self._concurrency-=1
          if(urlCount==0):
            plan = ssp.plan()
            ssp.resetUrls(plan)
        if(not urlFlag):
          time.sleep(3)
      except Exception as err:
        self.log(err,logging.ERROR)
        time.sleep(10)
      time.sleep(self._settingObj["intervalTime"])
    self._runflag=False
    self._pool.shutdown()
    self.log('simplified-scrapy stopped......')

  _concurrency=0
  _downloadPageNum=0
  _startCountTs=time.time()
  def checkConcurrency(self,name,count):
    tmSpan = time.time()-self._startCountTs
    if(tmSpan>10):
      if(self._downloadPageNum>(self._settingObj["concurrencyPer1S"]*tmSpan)):
        self.log('name={}, count={}, concurrency={}, downloadPageNum={}, tmSpan={}, reason={}'.format(name,count,self._concurrency,self._downloadPageNum,tmSpan,'exceed the config number CONCURRENCYPER1S'))
        return False
      self._startCountTs=time.time()
      self._downloadPageNum=0
    if self._concurrency >= self._settingObj["concurrency"]:
      self.log('name={}, count={}, concurrency={}, downloadPageNum={}, tmSpan={}, reason={}'.format(name,count,self._concurrency,self._downloadPageNum,tmSpan,'exceed the config number CONCURRENCY'))
      return False
    self._concurrency+=1
    self.log('name={}, count={}, concurrency={}, downloadPageNum={}, tmSpan={}'.format(name,count,self._concurrency,self._downloadPageNum,tmSpan))
    return True
  def _getTm(self, fileName):
    name = fileName.replace('.','/')+'.py'
    if isExistsFile(name):
      tm = getFileModifyTime(name)
      return tm
    return False
  def getSpider(self, fileName, className):
    try:
      logged_in = False
      if(fileName in self._spiderDic):
        oldSsp = self._spiderDic[fileName]
        logged_in = oldSsp.logged_in
        tm = self._getTm(fileName)
        if(not tm or oldSsp.tm == tm):
          return self._spiderDic[fileName]

        m = importlib.import_module(fileName)
        reload(m)
        cls = getattr(m, className)
        ssp = cls()
        ssp.logged_in = logged_in
        ssp.tm = tm
      else:
        m = importlib.import_module(fileName)
        cls = getattr(m, className)
        ssp = cls()
        ssp.tm = self._getTm(fileName)
      if not ssp.logged_in:
        ssp.logged_in = ssp.login()
      self._spiderDic[fileName]=ssp
      return ssp
    except Exception as err:
      self.log(err,logging.ERROR)

  def extractThread(self):
    while(self._runflag):
      flag=False
      for ssp in self._spiderDic.values():
        try:
          data = ssp.popHtml()
          if(not data):
            data = ssp.popHtml(2)

          if(data):
            flag = True
            obj = self._extracter.extract(data["url"],data["html"],ssp)
            if obj==True:
              ssp.updateHtmlState(data["id"],1)
            elif obj: 
              ssp.saveData(obj)
              ssp.updateHtmlState(data["id"],1)
            else:
              ssp.updateHtmlState(data["id"],2)
            if(ssp.models and len(ssp.models)>0):
              time.sleep(0.5)
            else:
              time.sleep(0.01)

        except Exception as err:
          self.log(err,logging.ERROR)
          time.sleep(10)
      if(not flag):
        time.sleep(3)
      time.sleep(1)
  def downloadThread(self,url,ssp):
    try:
      if(not url):
        return
      if(not isinstance(url,dict)):
        url={'url':url}
      printInfo(url['url'])
      self._downloadPageNum=self._downloadPageNum+1
      html = execDownload(url,ssp)
      if(html=="_error_"):
        # self._extracter.extract(url,html,ssp)
        # else:
        ssp.downloadError(url)
      else:
        ssp.saveHtml(url,html)
    except Exception as err:
      self.log(err,logging.ERROR)
    finally:
      self._concurrency-=1
  def down_callback(self,html,url,ssp):
    self._concurrency-=1
    if(not isinstance(url,dict)):
      url={'url':url}
    if(html=="_error_"):
      ssp.downloadError(url)
    elif html:
      ssp.saveHtml(url,html)
  def downloadRender(self,url,ssp):
    printInfo(url['url'])
    self._downloadPageNum+=1
    ssp.renderUrl(url,self.down_callback)

  def downloadThread2(self,*args):
    url=args[0]
    ssp=args[1]
    try:
      if(not url):
        return
      if(not isinstance(url,dict)):
        url={'url':url}
      printInfo(url['url'])
      self._downloadPageNum+=1

      html = execDownload(url,ssp)
      if(html=="_error_"):
        ssp.downloadError(url)
      else:
        ssp.saveHtml(url,html)
    except Exception as err:
      self.log(err,logging.ERROR)
    finally:
      self._concurrency-=1

SimplifiedMain = _SimplifiedMain()