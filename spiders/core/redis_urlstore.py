#!/usr/bin/python
#coding=utf-8
import redis,json,hashlib,random
class RedisUrlStore():
  _queueName = 'url_queue_'
  _setName = 'url_set_'
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
    self.pool = redis.ConnectionPool(host, port)
  def popUrl(self):
    r = redis.Redis(connection_pool=self.pool)
    num = random.randint(0,9)
    if(num<7):
      url = r.lpop(self._queueName)
    else:
      url = r.rpop(self._queueName)
    if(url):
      return json.loads(url)
    return None
  def getCount(self):
    r = redis.Redis(connection_pool=self.pool)
    return r.llen(self._queueName)
  def checkUrl(self,url):
    r = redis.Redis(connection_pool=self.pool)
    md5 = hashlib.md5(url).hexdigest()
    result = r.sadd(self._setName, md5)
    return not result
  def saveUrl(self, urls):
    r = redis.Redis(connection_pool=self.pool)
    # if (type(urls).__name__=='dict'):
    #   urls=urls["Urls"]
    for url in urls:
      if(isinstance(url,str)):
        url={'url':url}
      if(not self.checkUrl(url["url"])):
        r.rpush(self._queueName,json.dumps(url))
  def resetUrls(self, urls):
    r = redis.Redis(connection_pool=self.pool)
    for url in urls:
      if(isinstance(url,str)):
        url={'url':url}
      r.rpush(self._queueName,json.dumps(url))