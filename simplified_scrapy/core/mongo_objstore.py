#!/usr/bin/python
#coding=utf-8
from pymongo import MongoClient
class MongoObjStore:
  _host='127.0.0.1'
  _port=27017
  _dbName='python_db'
  _tbName='obj_'
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

  def saveObj(self, data):
    objs = data.get("Datas")
    if(objs != None):
      if(objs):
        db = self._connect()
        db[self._tbName].insert(data)
    elif isinstance(data, dict):
      db = self._connect()
      db[self._tbName].insert(data)