#!/usr/bin/python
#coding=utf-8
from pymongo import MongoClient
import json,hashlib,random,random
from utils import convert2Int
class MongoUrlStore():
  _host = '127.0.0.1'
  _port = 27017
  _dbName = 'python_db'
  _tbName = 'url_'
  _multiQueue = False
  def __init__(self,name, setting=None):
    self._tbName = self._tbName+name
    if(setting):
      if(setting.get('host')):
        self._host=setting.get('host')
      if(setting.get('port')):
        self._port=setting.get('port')
      if(setting.get('dbName')):
        self._dbName=setting.get('dbName')
      if(setting.get('tbName')):
        self._tbName=setting.get('tbName')
      if(setting.get('multiQueue')):
        self._multiQueue = setting.get('multiQueue')
  def _connect(self):
    conn = MongoClient(self._host, self._port)
    return conn[self._dbName]

  def popUrl(self):
    db = self._connect()
    lst=[]
    while(True):
      if(lst.count==10): return None
      tbName = self._tbName
      i = random.randint(0,9)
      print 'popUrl',i
      if(i in lst): continue
      lst.append(i)
      if(i):
        tbName = tbName+str(i)
      url = db[tbName].find_one({"state": 0})
      if(url): db[tbName].update({"_id": url["_id"]}, {"$set": {"state": 1}})
      return url

  def getCount(self):
    db = self._connect()
    return db[self._tbName].find({"state": 0}).count()

  def checkUrl(self,url,i):
    db = self._connect()
    id = hashlib.md5(url).hexdigest()
    tbName = self._tbName
    url = db[tbName].find_one({"_id": id})
    if(not url and i):
      tbName = tbName+str(i)
      url = db[tbName].find_one({"_id": id})
    return url

  def saveUrl(self, urls,i=None):
    db = self._connect()
    for url in urls:
      if(isinstance(url,str)):
        id = hashlib.md5(url).hexdigest()
        url = {'url':url, '_id':id, 'state':0}
      else:
        id = hashlib.md5(url["url"]).hexdigest()
        url['_id']=id
        url['state']=0
      if(i != 0):
        i = self._getIndex(url["url"])
      if(not self.checkUrl(url["url"],i)):
        tbName = self._tbName
        if(i):
          tbName = tbName+str(i)
        db[tbName].insert(url)
  def _getIndex(self, url):
    if(not self._multiQueue or not url): return None
    return convert2Int(url)

  def resetUrls(self, urls):
    db = self._connect()
    for url in urls:
      if(isinstance(url,str)):
        id = hashlib.md5(url).hexdigest()
        url={'url':url,'_id':id, 'state':0}
      else:
        id = hashlib.md5(url["url"]).hexdigest()
        url['_id']=id
        url['state']=0
      if(not self.checkUrl(url["url"],None)):
        db[self._tbName].insert(url)
      else:
        db[self._tbName].update({"_id": url["_id"]}, {"$set": {"state": 0}})
