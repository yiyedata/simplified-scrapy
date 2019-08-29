#!/usr/bin/python
#coding=utf-8
from pymongo import MongoClient
from core.request_helper import requestPost
class HttpObjStore:
  _url='127.0.0.1/api'
  _key='yiyedata_test'
  def __init__(self, name):
    pass
  
  def saveObj(self, data):
    objs = data.get("Datas")
    if(objs and len(objs)>0):
      requestPost(self._url, {'key':self._key, 'data':data},{ "Content-Type": "application/json"})