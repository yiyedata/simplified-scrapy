#!/usr/bin/python
#coding=utf-8
from core.mongo_urlstore import MongoUrlStore
class MeishiUrlStore(MongoUrlStore):
  def saveUrl(self, urls):
    data=[]
    for u in urls:
      if(isinstance(u,str)):
        u = {'url':u}
      url = u['url']
      if(url.find('Health/')>0 or url.find('jiankang/')>0 
        or url.find('xinxianzixun')>0 or url.find('shipinanquan')>0 
        or url.find('wenhua')>0 or url.find('yangsheng')>0 or url.find('zuofa')>0
        or url.find('/a/')>0 or url.find('tag/19581')>0 or url.find('tag/19580')>0
        or url.find('tag/68062')>0 or url.find('tag/68060')>0 or url.find('tag/19577')>0
        or url.find('tag/20846')>0 or url.find('tag/22547')>0 or url.find('tag/77843')>0
        or url.find('chihe.sohu')>0
        or url.find('douguo.com')>0 or url.find('meishic.com/')>0 or url.find('zl/eat/')>0
        or url.find('ttmeishi.com')>0
        or url.find('someishi.com')>0):
        # 'tag/68062,68060,19577,20846,22547,77843'
        if(url.find('/Video')>0): continue
        data.append(u)
    MongoUrlStore.saveUrl(self,data)