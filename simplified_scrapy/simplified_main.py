#!/usr/bin/python
#coding=utf-8
import logging
import simplified_scrapy.core.logex
import threading,traceback,time,importlib,imp,os,json,io
from imp import reload
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
      self._settingObj = {}
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
              dicTmp.append(spider['file'])
              self.getSpider(spider['file'],spider["class"])
            except Exception as err:
              self.log(err,logging.ERROR)

          keys = self._spiderDic.keys()
          for key in keys:
            if(key not in dicTmp):
              del self._spiderDic[key]
      else:
        settingObj = {}
      if(self.singleSSP): self._spiderDic[self.singleSSP.name] = self.singleSSP

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
  _spiderDic = {}
  def startThread(self,ssp=None):
    if(self._started): return
    self._started = True

    self._init(ssp)
    threadExtract = threading.Thread(target=self.extractThread)
    threadExtract.start()
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
          if(not ssp): continue
          urlCount = ssp.urlCount()
          if(self.checkConcurrency(ssp.name,urlCount)):
            url = ssp.popUrl()
            if(url):
              urlFlag = True
              self.downloadCount+=1
              if(not isinstance(url,str) and url.get("requestMethod")=="render"):
                self._downloadPageNum+=1
                ssp.renderUrl(url,self.down_callback)
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
      if(fileName in self._spiderDic):
        oldSsp = self._spiderDic[fileName]
        tm = self._getTm(fileName)
        if(not tm or oldSsp.tm == tm):
          return self._spiderDic[fileName]

        m = importlib.import_module(fileName)
        reload(m)
        cls = getattr(m, className)
        ssp = cls()
        ssp.tm = tm
      else:
        m = importlib.import_module(fileName)
        cls = getattr(m, className)
        ssp = cls()
        ssp.tm = self._getTm(fileName)

      flag = False
      i = 3
      while(i>0):
        flag = ssp.login()
        if(flag): break
        i=i-1
      if(flag):
        self._spiderDic[fileName]=ssp
      else:
        printInfo(className +': login failed')
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
            if obj: 
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
      if(isinstance(url,str)):
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
    if(isinstance(url,str)):
      url={'url':url}
    if(html=="_error_"):
      ssp.downloadError(url)
    elif html:
      ssp.saveHtml(url,html)
  def downloadThread2(self,*args):
    url=args[0]
    ssp=args[1]
    try:
      if(not url):
        return
      if(isinstance(url,str)):
        url={'url':url}
      printInfo(url['url'])
      self._downloadPageNum+=1

      # if(not isinstance(url,str) and url.get("requestMethod")=="render"):
      #   ssp.renderUrl(url,self.down_callback)
      # else:
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