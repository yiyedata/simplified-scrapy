#!/usr/bin/python
#coding=utf-8
import json
from logPrint import appendFile
class ObjStore:
  def saveObj(self, data):
    objs=data.get("Datas")
    if(objs and len(objs)>0):
      appendFile('obj.json', json.dumps(objs))