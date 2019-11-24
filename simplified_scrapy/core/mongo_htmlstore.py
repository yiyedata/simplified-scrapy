#!/usr/bin/python
#coding=utf-8
from pymongo import MongoClient
class MongoHtmlStore:
  _host='127.0.0.1'
  _port=27017
  _dbName='python_db'
  _tbName='html_'
  def __init__(self, name, setting=None):
    self._tbName = self._tbName + name
    if(setting):
      if(setting.get('host')):
        self._host=setting.get('host')
      if(setting.get('port')):
        self._port=setting.get('port')
      if(setting.get('dbName')):
        self._dbName=setting.get('dbName')
      if(setting.get('tbName')):
        self._tbName=setting.get('tbName')

  def _connect(self):
    conn = MongoClient(self._host, self._port)
    return conn[self._dbName]

  def saveHtml(self,url,html):
    if(not html): return False
    db = self._connect()
    # if(isinstance(url,str)):
    #   id = hashlib.md5(url).hexdigest()
    # else:
    #   id = hashlib.md5(url["url"]).hexdigest()
    db[self._tbName].insert({"url":url, "html":html, "state":0})

  def updateState(self,id,state):
    db = self._connect()
    # if(isinstance(url,str)):
    #   id = hashlib.md5(url).hexdigest()
    # else:
    #   id = hashlib.md5(url["url"]).hexdigest()
    db[self._tbName].update({"_id": id}, {"$set": {"state": state}})

  def popHtml(self,state=0):
    db = self._connect()
    obj = db[self._tbName].find_one({"state": state})
    obj["id"]=obj["_id"]
    return obj
