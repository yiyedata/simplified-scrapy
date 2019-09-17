#!/usr/bin/python
#coding=utf-8
import io,json,hashlib,os
from threading import Lock
class UrlStore:
  _urls=[]
  _i=0
  _dic=set()
  _urlFilename = 'db/{}-urls.yd'
  _dicFilename = 'db/{}-dic.yd'
  _indexFilename = 'db/{}-index.yd'
  _lock = Lock()
  def __init__(self, name):
    try:
      self._urlFilename=self._urlFilename.format(name)
      self._dicFilename=self._dicFilename.format(name)
      self._indexFilename=self._indexFilename.format(name)
      if(not os.path.exists('db/')):
        os.mkdir('db/')
      self._urlfile = io.open(self._urlFilename, "a+",encoding="utf-8")
      self._dicfile = io.open(self._dicFilename, "a+",encoding="utf-8")
      self._indexfile = io.open(self._indexFilename, "a+",encoding="utf-8")
      self._urlfile.seek(0)
      self._dicfile.seek(0)
      self._indexfile.seek(0)
      index = self._indexfile.read()
      if(index):
        self._i = int(index)
      line = 'start'
      while(line):
        line = self._dicfile.readline()
        if(line):
          self._dic.add(line[:-1])
      i = 0
      line = 'start'
      while(line):
        line = self._urlfile.readline()
        if(i<self._i):
          i=i+1
          continue
        if(line):
          self._urls.append(json.loads(line[:-1]))
    except Exception as err:
      print err 
      
  def __del__(self):
    self._urlfile.close()
    self._dicfile.close()
    self._indexfile.close()
    print '__del__'

  def popUrl(self):
    url=None
    if(len(self._urls)>0):
      url=self._urls.pop()
      self._i = self._i+1
      self._indexfile.seek(0)
      self._indexfile.truncate()
      self._indexfile.write(u'{}'.format(self._i))
      self._indexfile.flush()
    return url

  def getCount(self):
    return len(self._urls)

  def checkUrl(self,url):
    md5=hashlib.md5(url).hexdigest()
    return md5 in self._dic

  def saveUrl(self, urls,i=None):
    # if (type(urls).__name__=='dict'):
    #   urls=urls["Urls"]
    self._lock.acquire()
    try:
      flag=False
      for url in urls:
        if(isinstance(url,str)):
          url={'url':url}
        md5=hashlib.md5(url['url']).hexdigest()
        if(md5 not in self._dic):
          self._urls.append(url)
          self._dic.add(md5)
          self._writeFile(url,md5)
          flag=True
      if(flag):
        self._flushFile()
    except Exception as err:
      print err
    finally:
      self._lock.release()

  def _flushFile(self):
    self._dicfile.flush()
    self._urlfile.flush()

  def _writeFile(self, url, md5):
    self._dicfile.write(u'{}\n'.format(md5))
    self._urlfile.write(u'{}\n'.format(json.dumps(url)))
  
  def resetUrls(self, urls):
    self._lock.acquire()
    try:
      flag=False
      for url in urls:
        if(isinstance(url,str)):
          url={'url':url}
        md5=hashlib.md5(url['url']).hexdigest()
        self._urls.append(url)
        self._dic.add(md5)
        self._writeFile(url,md5)
        flag=True
      if(flag):
        self._flushFile()
    except Exception as err:
      print err
    finally:
      self._lock.release()
