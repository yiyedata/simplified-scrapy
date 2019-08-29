#!/usr/bin/python
#coding=utf-8
import time
from pymongo import MongoClient
from core.request_helper import requestPost
class MongoObjStore:
  _host='127.0.0.1'
  _port=27017
  _dbName='python_db'
  _tbName='obj_'
  _url='127.0.0.1/api'
  _key='yiyedata_test'
  def __init__(self, name):
    self._tbName = self._tbName + name
  def _connect(self):
    conn = MongoClient(self._host, self._port)
    return conn[self._dbName]

  def exportObj(self):
      db = self._connect()
      while True:
        objs = db[self._tbName].find({"state":{ "$exists": False }})
        for obj in objs:
          try:
            self._exportObj(obj)
            db[self._tbName].update({"_id": obj["_id"]}, {"$set": {"state": 1}})
            time.sleep(0.3)
          except Exception as err:
            print err
        time.sleep(5)

  def _exportObj(self,data):
    print data["_id"]
    requestPost(self._url, {'key':self._key, 'data':data},{ "Content-Type": "application/json"})

test = MongoObjStore('tb')
test.exportObj()