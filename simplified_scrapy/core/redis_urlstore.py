#!/usr/bin/python
#coding=utf-8
import redis,json,random
import sys
from simplified_scrapy.core.utils import printInfo,convertUrl2Int,md5

class RedisUrlStore():
  _queueName = 'url_queue_'
  _setName = 'url_set_'
  _multiQueue = False
  def __init__(self, name, setting=None):
    self._queueName=self._queueName+name
    self._setName=self._setName+name
    host = '127.0.0.1'
    port = 6379
    if(setting):
      if(setting.get('host')):
        host=setting.get('host')
      if(setting.get('port')):
        port=setting.get('port')
      if(setting.get('queueName')):
        self._queueName=setting.get('queueName')
      if(setting.get('setName')):
        self._setName=setting.get('setName')
      if(setting.get('multiQueue')):
        self._multiQueue = setting.get('multiQueue')
    self.pool = redis.ConnectionPool(host, port)
  def popUrl(self):
    r = redis.Redis(connection_pool=self.pool)
    lst=[]
    while(True):
      if(lst.count==10): return None
      tbName = self._queueName
      i = random.randint(0,9)
      if(i in lst): continue
      lst.append(i)
      if(i):
        tbName=tbName+str(i)
      url = r.lpop(tbName)
      if(url):
        return json.loads(url)
    return None
  def getCount(self):
    r = redis.Redis(connection_pool=self.pool)
    return r.llen(self._queueName)
  def checkUrl(self,url):
    r = redis.Redis(connection_pool=self.pool)
    result = r.sadd(self._setName, md5(url))
    return not result
  def saveUrl(self, urls,i=None):
    r = redis.Redis(connection_pool=self.pool)
    # if (type(urls).__name__=='dict'):
    #   urls=urls["Urls"]
    for url in urls:
      if(isinstance(url,str)):
        url={'url':url}
      if(not self.checkUrl(url["url"])):
        if(i != 0):
          i = self._getIndex(url["url"])
        tbName = self._queueName
        if(i):
          tbName = tbName+str(i)
        r.rpush(tbName,json.dumps(url))
  
  def _getIndex(self, url):
    if(not self._multiQueue or not url): return None
    return convertUrl2Int(url)

  def resetUrls(self, urls):
    r = redis.Redis(connection_pool=self.pool)
    for url in urls:
      if(isinstance(url,str)):
        url={'url':url}
      r.rpush(self._queueName,json.dumps(url))
  
  def updateState(self, url, state):
    pass