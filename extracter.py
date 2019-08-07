#!/usr/bin/python
#coding=utf-8
import json,re,importlib,os
from spiders.core.request_helper import extractHtml

class Extracter:
  _models={}
  def __init__(self):
    #读文件
    fileName = os.path.realpath(__file__)
    rootdir = os.path.dirname(fileName)
    if(rootdir[-1]=='/' or rootdir[-1]=='\\'):
      rootdir = rootdir +'models/'
    else:
      rootdir = rootdir +'/models/'
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
      name = list[i]
      path = os.path.join(rootdir,name)
      if os.path.isfile(path):
        f = open(path,'r')
        print 'Extracter.name',name
        self._models[name[:-5]] = json.loads(f.read().decode('utf-8'))
        f.close()
    print 'Extracter._models',self._models

  def extract(self,url,html,ssp):
    models=[]
    for modelName in ssp.models:
      models.append(self._models[modelName])
    
    data = extractHtml(url["url"],html,models,ssp.models,url.get("title"),ssp)
    ssp.saveData(data)

# print  os.path.abspath(os.curdir)+'/simplified-scrapy/models/'
# print os.path.abspath('..')