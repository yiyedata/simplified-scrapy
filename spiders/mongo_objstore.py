#!/usr/bin/python
#coding=utf-8
from pymongo import MongoClient
class MongoObjStore:
  _host='127.0.0.1'
  _port=27017
  _dbName='python_db'
  _tbName='obj_'
  def __init__(self, name):
    self._tbName = self._tbName + name
  def _connect(self):
    conn = MongoClient(self._host, self._port)
    return conn[self._dbName]

  def saveObj(self, data):
    objs = data.get("Datas")
    if(objs and len(objs)>0):
      db = self._connect()
      db[self._tbName].insert(data)