#!/usr/bin/python
#coding=utf-8
import socket,time
from pymongo import MongoClient
class MongoHtmlStore:
  _host='127.0.0.1'
  _port=27017
  _dbName='python_db'
  _tbName='html_'
  _lockTb='lock_smps'
  _lockKey=_lockTb+'_'
  _enableLock=False
  _appName=None
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
      if(setting.get('appName')):
        self._appName=setting.get('appName')
      if(setting.get('enableLock')):
        self._enableLock=setting.get('enableLock')
      self._lockKey = self._lockKey + self._tbName
      if self._enableLock:
        try:
          if not self._appName:
            self._appName=socket.gethostbyname(socket.getfqdn(socket.gethostname()))
          db = self._connect()
          obj = db[self._lockTb].find_one({"_id": self._lockKey})
          if not obj:
            db[self._lockTb].insert_one({"_id":self._lockKey,"state":0})
        except Exception as err:
          print (err)
  def _connect(self):
    conn = MongoClient(self._host, self._port)
    return conn[self._dbName]

  def saveHtml(self,url,html):
    if(not html): return False
    db = self._connect()
    db[self._tbName].insert({"url":url, "html":html, "state":0})

  def updateState(self,id,state):
    db = self._connect()
    db[self._tbName].update_one({"_id": id}, {"$set": {"state": state}})
  _lockCount=0
  def _getLock(self):
    if not self._enableLock: return True
    db = self._connect()
    result = db[self._lockTb].update_one({"_id":self._lockKey,
      "$or":[{"state":0},{"owner":self._appName},{"tm":{"$lt":time.time()-3*60}}]}, 
      {"$set": {"state": 1,"owner":self._appName,"tm":time.time()}})
    return result.modified_count

  def _releaseLock(self):
    if not self._enableLock: return True
    db = self._connect()
    result = db[self._lockTb].update_one({"_id":self._lockKey, "state":1, "owner":self._appName}, {"$set": {"state": 0}})
    return result.modified_count
  def popHtml(self,state=0):
    lk = self._getLock()
    if lk:
      return self._popHtml(state)
    return None

  def _popHtml(self,state):
    try:
      db = self._connect()
      obj = db[self._tbName].find_one({"state": state})
      if obj:
        obj["id"]=obj["_id"]
        if self._enableLock: self.updateState(obj["id"],3)
      self._releaseLock()
      return obj
    except Exception as err:
      self._releaseLock()
      print (err)
if __name__ == '__main__':
  test = MongoHtmlStore('test',{"enableLock":1})
  flag = test._getLock()
  falg = test._releaseLock()