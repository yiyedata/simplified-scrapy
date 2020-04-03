#!/usr/bin/python
#coding=utf-8
import json,os
import sys
from simplified_scrapy.core.utils import appendFile
from simplified_scrapy.core.objstore_base import ObjStoreBase
class ObjStore(ObjStoreBase):
  _objFilename='data/{}_obj.json'
  def __init__(self, name):
    self._objFilename=self._objFilename.format(name)
    if(not os.path.exists('data/')):
      os.mkdir('data/')
  def saveObj(self, data):
    if isinstance(data, dict):
      objs = data.get("Datas")
      if(objs != None):
        if(objs):
          appendFile(self._objFilename, json.dumps(objs,ensure_ascii=False))
      appendFile(self._objFilename, json.dumps(data,ensure_ascii=False))
    else:
      appendFile(self._objFilename, data)