#!/usr/bin/python
#coding=utf-8
import json
from core.logPrint import logPrint,logError,getTime,appendFile
from core.spider import Spider 
class TestSpider(Spider):
  name = 'test-spider'
  start_urls = ['http://health.sohu.com/','http://health.sina.com.cn/','http://www.39.net/']
  models = ['auto_all','auto_obj']

  def afterResponse(self, response, cookie, url):
    html = Spider.afterResponse(self,response,cookie,url)
    return Spider.removeScripts(self,html)

  def saveObj(self, data):
    d = data.get("Data")
    if(d and len(d) > 0):
      objs=d[0].get("Datas")
      if(objs and len(objs)>0):
        appendFile('obj.json', json.dumps(objs))
    

  # def saveUrl(self, data):
  #   saveFile('url.json', data)