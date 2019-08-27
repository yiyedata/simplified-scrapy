#!/usr/bin/python
#coding=utf-8
from pymongo import MongoClient
import json,hashlib,random
class MongoUrlStore():
  _host = '127.0.0.1'
  _port = 27017
  _dbName = 'python_db'
  _tbName = 'url_'

  def __init__(self,name):
    self._tbName = self._tbName+name

  def _connect(self):
    conn = MongoClient(self._host, self._port)
    return conn[self._dbName]

  def popUrl(self):
    db = self._connect()
    url = db[self._tbName].find_one({"state": 0})
    if(url): db[self._tbName].update({"_id": url["_id"]}, {"$set": {"state": 1}})
    return url

  def getCount(self):
    db = self._connect()
    return db[self._tbName].find({"state": 0}).count()

  def checkUrl(self,url):
    db = self._connect()
    id = hashlib.md5(url).hexdigest()
    url = db[self._tbName].find_one({"_id": id})
    return url

  def saveUrl(self, urls):
    db = self._connect()
    for url in urls:
      if(isinstance(url,str)):
        id = hashlib.md5(url).hexdigest()
        url={'url':url,'_id':id, 'state':0}
      else:
        id = hashlib.md5(url["url"]).hexdigest()
        url['_id']=id
        url['state']=0
      if(not self.checkUrl(url["url"])):
        db[self._tbName].insert(url)
        
