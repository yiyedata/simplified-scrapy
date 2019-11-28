#!/usr/bin/python
#coding=utf-8
try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET
import sys,re
from simplified_scrapy.core.utils import printInfo
from simplified_scrapy.core.dictex import Dict
class XmlDictConfig(dict):
  def __init__(self, parent_element):
    if parent_element.items():
      self.update(dict(parent_element.items()))
      self['text'] = parent_element.text
    flag = False
    for element in parent_element:
      flag = True
      if(not self.get(element.tag)):
        self.update({element.tag: []})

      dic = self.getDic(element)
      self[element.tag].append(dic)
      count = len(element)
      if(count>0):
        self.ele2arr(dic,element)
    if(not flag):
      self.update({'tag':parent_element.tag, 'text':parent_element.text})

  def getDic(self,element):
    if element.items():
      dic = dict(element.items())
      dic['text'] = element.text
    else:
      dic={'text':element.text}
    return dic

  def ele2arr(self,dic,elements):
    if(not dic.get("children")):
      dic["children"] = {}
    if(not dic["text"]):
      dic["text"]=""
    for element in elements:
      if( not dic["children"].get(element.tag)):
        dic["children"].update({element.tag:[]})
      if(element.text):
        dic["text"] = dic["text"]+element.text
      if(element.tail):
        dic["text"] = dic["text"]+element.tail
      dic["children"][element.tag].append(self.getDic(element))

  def __getattr__(self,attr):
    if(self.get(attr)):
      return self.get(attr)
    else:
      return None

  def __getitem__(self,attr):
    if(self.get(attr)):
      return self.get(attr)
    else:
      return None

def convert2Dic(html):
  try:
    html = re.sub('(\\s|&nbsp;)+', ' ', html, 0)
    start = html.find('<')
    end = html.find('>')
    paras = html[start+1:end].strip('/').split()
    dic = Dict()
    first = True
    for para in paras:
      if(first):
        first=False
        dic['tag']=para
        continue
      kv=para.split('=')
      key = kv[0].strip()
      if(len(kv)==1):
        if(not dic[key]): dic[key]=""
      else:
        if(not dic[key]): 
          dic[key]=kv[1].strip().strip('"').strip('\'')
        else: 
          dic[key]+=' ' 
          dic[key]+=kv[1].strip().strip('"').strip('\'')
    return dic
    # tree = ET.XML(html)
    # return XmlDictConfig(tree)
  except Exception as err:
    printInfo(err)
  return None

# print (convert2Dic('<div class="container" id="app" class="page-board/index" />test</div>'))