#!/usr/bin/python
#coding=utf-8
import core
import redis,json
class RedisUrlStore():
  _queueName = 'url_queue_python'
  _setName = 'url_set_python'
  def __init__(self):
    self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    
  def popUrl(self):
    r = redis.Redis(connection_pool=self.pool)
    url = r.lpop(self._queueName)
    if(url):
      return json.loads(url)
    return None
  def getCount(self):
    r = redis.Redis(connection_pool=self.pool)
    return r.llen(self._queueName)
  def checkUrl(self,url):
    r = redis.Redis(connection_pool=self.pool)
    result = r.sadd(self._setName,url)
    return not result
  def saveUrl(self, urls):
    r = redis.Redis(connection_pool=self.pool)
    if (type(urls).__name__=='dict'):
      urls=urls["Urls"]
    for url in urls:
      if(isinstance(url,str)):
        url={'url':url}
      if(not self.checkUrl(url["url"])):
        r.rpush(self._queueName,json.dumps(url))
        
