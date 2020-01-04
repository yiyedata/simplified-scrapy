#!/usr/bin/python
#coding=utf-8
from pymongo import MongoClient
import json,random,random
import sys
from simplified_scrapy.core.utils import printInfo,convertUrl2Int,md5

class MongoUrlStore():
  _host = '127.0.0.1'
  _port = 27017
  _dbName = 'python_db'
  _tbName = 'url_'
  _dicName = 'dic_'
  _multiQueue = False
  _tbCache = {}
  _totalCount = {}
  def __init__(self,name, setting=None):
    self._tbName = self._tbName+name
    self._dicName = self._dicName+name
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
      printInfo('popUrl',i)
      if(i in lst): continue
      lst.append(i)
      if(i):
        tbName = tbName+str(i)
      if(self._tbCache.get(tbName)): continue
        
      url = db[tbName].find_one({"state": 0})
      if(url): 
        db[tbName].update({"_id": url["_id"]}, {"$set": {"state": 1}})
        if(i in self._totalCount): self._totalCount[i] -= 1
      else:
        self._tbCache[tbName] = True
      return url

  def getCount(self):
    db = self._connect()
    i = 1
    if(0 not in self._totalCount):
      self._totalCount[0]=db[self._tbName].find({"state": 0}).count()
    total = self._totalCount[0]
    while(i<10):
      if(i not in self._totalCount):
        self._totalCount[i]=db[self._tbName+str(i)].find({"state": 0}).count()
      total += self._totalCount[i]
    return total

  def checkUrl(self,url,i):
    db = self._connect()
    id = md5(url)
    tbName = self._tbName

    if(i): tbName = tbName + str(i)
    url = db[tbName].find_one({"_id": id})
    if(not url and not i):
      url = db[self._tbName].find_one({"_id": id})
    return url

  def saveUrl(self, urls,i=None):
    db = self._connect()
    flag = False
    for url in urls:
      if(not isinstance(url,dict)):
        id = md5(url)
        url = {'url':url, '_id':id, 'state':0}
      else:
        id = md5(url["url"])
        url['_id']=id
        url['state']=0
      if(i != 0):
        i = self._getIndex(url["url"])
      if(not self.checkUrl(url["url"],i)):
        tbName = self._tbName
        if(i):
          tbName = tbName+str(i)
        db[tbName].insert(url)
        if(i in self._totalCount): self._totalCount[i]+=1
        else: self._totalCount[i] = 1
        flag = True
    if(flag):
      self._tbCache[tbName] = False
      
  def _getIndex(self, url):
    if(not self._multiQueue or not url): return None
    return convertUrl2Int(url)

  def resetUrls(self, urls):
    db = self._connect()
    for url in urls:
      if(not isinstance(url,dict)):
        id = md5(url)
        url={'url':url,'_id':id, 'state':0}
      else:
        id = md5(url["url"])
        url['_id']=id
        url['state']=0
      if(not self.checkUrl(url["url"],None)):
        db[self._tbName].insert(url)
      else:
        db[self._tbName].update({"_id": url["_id"]}, {"$set": {"state": 0}})

  def updateState(self, url, state):
    db = self._connect()
    if(not isinstance(url,dict)):
      id = md5(url)
    else:
      id = md5(url["url"])
    db[self._tbName].update({"_id": id}, {"$set": {"state": state}})