#!/usr/bin/python
#coding=utf-8
import hashlib
from pymongo import MongoClient
class MongoHtmlStore:
  _host='127.0.0.1'
  _port=27017
  _dbName='python_db'
  _tbName='html_'
  def __init__(self, name):
    self._tbName = self._tbName + name
  def _connect(self):
    conn = MongoClient(self._host, self._port)
    return conn[self._dbName]

  def saveHtml(self,url,html):
    if(not html): return False
    db = self._connect()
    if(isinstance(url,str)):
      id = hashlib.md5(url).hexdigest()
    else:
      id = hashlib.md5(url["url"]).hexdigest()
    db[self._tbName].insert({"_id":id, "url":url, "html":html, "state":0})

  def updateState(self,url,state):
    db = self._connect()
    if(isinstance(url,str)):
      id = hashlib.md5(url).hexdigest()
    else:
      id = hashlib.md5(url["url"]).hexdigest()
    db[self._tbName].update({"_id": id}, {"$set": {"state": state}})

  def popHtml(self):
    db = self._connect()
    return db[self._tbName].find_one({"state": 0})
