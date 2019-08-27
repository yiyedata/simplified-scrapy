#!/usr/bin/python
#coding=utf-8
from mongo_urlstore import MongoUrlStore
class MeishiUrlStore(MongoUrlStore):
  def saveUrl(self, urls):
    data=[]
    for u in urls:
      if(isinstance(u,str)):
        u = {'url':u}
      url = u['url']
      if(url.find('Health/')>0 or url.find('jiankang/')>0 
        or url.find('xinxianzixun')>0 or url.find('shipinanquan')>0 
        or url.find('wenhua')>0 or url.find('yangsheng')>0 or url.find('zuofa')>0):
        data.append(u)
    MongoUrlStore.saveUrl(self,data)