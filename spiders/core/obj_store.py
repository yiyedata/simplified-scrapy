#!/usr/bin/python
#coding=utf-8
import json,os
from utils import appendFile
class ObjStore:
  _objFilename='data/{}_obj.json'
  def __init__(self, name):
    self._objFilename=self._objFilename.format(name)
    if(not os.path.exists('data/')):
      os.mkdir('data/')
  def saveObj(self, data):
    objs = data.get("Datas")
    if(objs and len(objs)>0):
      appendFile(self._objFilename, json.dumps(objs,ensure_ascii=False))