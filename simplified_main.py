#!/usr/bin/python
#coding=utf-8
import threading,traceback,time,importlib,imp,os,logging
from spiders.core.log import Log
from downloader import execDownload
from extracter import Extracter
from setting import SPIDERS,CONCURRENCY,CONCURRENCYPER1S
class SimplifiedMain(Log):
  def __init__(self):
    Log.__init__(self,'simplified-main')
    for spider in SPIDERS:
      try:
        self.getSpider(spider['file'],spider["class"])
      except Exception as err:
        self.log(err,logging.ERROR)

  _runflag = False
  def setRunFlag(self, flag):
    self._runflag = flag

  _spiderDic = {}
  _extracter = Extracter()
  def startThread(self):
    while self._runflag:
      try:
        for ssp in self._spiderDic.values():
          if(self.checkConcurrency()):
            thread = threading.Thread(target=self.downloadThread, args=(ssp.getUrl(),ssp))
            thread.start()
      except Exception as err:
        self.log(err,logging.ERROR)
        time.sleep(10)
      time.sleep(0.7)
    self._runflag=False
    self.log('download app stoped......')

  _concurrency=0
  _downloadPageNum=0
  _startCountTs=time.time()
  def checkConcurrency(self):
    tmSpan = time.time()-self._startCountTs
    if(tmSpan>10):
      if(self._downloadPageNum>(CONCURRENCYPER1S*tmSpan)):
        self.log('downloadPageNum={}, tmSpan={}'.format(self._downloadPageNum,tmSpan))
        return False
      self._startCountTs=time.time()
      self._downloadPageNum=0
    if self._concurrency > CONCURRENCY:
      self.log('concurrency={}'.format(self._concurrency))
      return False
    self._concurrency+=1
    self.log('concurrency={}, downloadPageNum={}, tmSpan={}'.format(self._concurrency,self._downloadPageNum,tmSpan))
    return True

  def getSpider(self, fileName, className):
    if(fileName in self._spiderDic):
      return self._spiderDic[fileName]
    m = importlib.import_module(fileName,'spiders')
    cls = getattr(m, className)
    ssp = cls()
    self._spiderDic[fileName]=ssp
    return ssp

  def downloadThread(self,url,ssp):
    try:
      if(not url):
        return
      if(isinstance(url,str)):
        url={'url':url}
      print url['url']
      self._downloadPageNum=self._downloadPageNum+1
      html = execDownload(url,ssp)
      if(html):
        self._extracter.extract(url,html,ssp)
      else:
        ssp.downloadError(url)
    except Exception as err:
        self.log(err,logging.ERROR)
    finally:
      self._concurrency-=1

thrc = SimplifiedMain()
thrc.setRunFlag(True)
thrc.startThread()