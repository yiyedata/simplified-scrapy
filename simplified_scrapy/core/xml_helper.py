#!/usr/bin/python
#coding=utf-8
try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET
import sys,re
from simplified_scrapy.core.utils import printInfo
from simplified_scrapy.core.dictex import Dict
class XmlDictConfig(Dict):
  def __init__(self, parent_element):
    if parent_element.items():
      self.update(Dict(parent_element.items()))
      # self['text'] = parent_element.text
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
      self.update({'tag':parent_element.tag})#, 'text':parent_element.text})

  # def getDic(self,element):
  #   if element.items():
  #     dic = dict(element.items())
  #     dic['text'] = element.text
  #   else:
  #     dic={'text':element.text}
  #   return dic

  # def ele2arr(self,dic,elements):
  #   if(not dic.get("children")):
  #     dic["children"] = {}
  #   if(not dic["text"]):
  #     dic["text"]=""
  #   for element in elements:
  #     if( not dic["children"].get(element.tag)):
  #       dic["children"].update({element.tag:[]})
  #     if(element.text):
  #       dic["text"] = dic["text"]+element.text
  #     if(element.tail):
  #       dic["text"] = dic["text"]+element.tail
  #     dic["children"][element.tag].append(self.getDic(element))

  # def __getattr__(self,attr):
  #   if(self.get(attr)):
  #     return self.get(attr)
  #   else:
  #     return None

  # def __getitem__(self,attr):
  #   if(self.get(attr)):
  #     return self.get(attr)
  #   else:
  #     return None

def convert2Dic(html):
  try:
    tag=''
    if(html.find('</')<0 and html.find('/>')<0):
      start = html.find('<')
      end = html.find(' ',start+1)
      tag = '</'+html[start+1:end]+'>'
    tree = ET.XML(html+tag)
    return XmlDictConfig(tree)
  except Exception as err:
    try:
      start = html.find('<')
      end = html.find('>')
      html = html[start+1:end].strip('/').strip()
      html = re.sub('(\\s|&nbsp;)+', ' ', html, 0)
      html = re.sub('(\')+', '"', html, 0)
      html = re.sub('(=\s*")+', '="', html, 0)
      lstC = []#list(html)
      N=len(html)
      i=0
      first = False
      flag = False
      while i<N:
        if html[i]=='"':
          lstC.append(html[i])
          first = not first
        elif not first and html[i]=='=' and html[i+1]!='"':
          lstC.append(html[i])
          lstC.append('"')
          flag=True
        elif not first and flag and html[i]==' ':
          flag=False
          lstC.append('"')
          lstC.append(html[i])
        else:
          lstC.append(html[i])
        i+=1
      html = ''.join(lstC)
      paras = html.split('"')
      dic = Dict()
      lastP=None
      first = True
      for para in paras:
        if(first):
          first=False
          tmp=para.split()
          dic['tag']=tmp[0]
          if(len(tmp)>1):
            lastP=tmp[1].strip().strip('=').strip()
          continue
        if(lastP):
          if(not dic[lastP]): 
            dic[lastP]=para
          else:
            dic[lastP]+=' '
            dic[lastP]+=para
          lastP=None
        elif para:
          if(para.find('=')>0):
            lastP=para.strip().strip('=').strip()
          else:
            dic[para]=''
      return dic
    except Exception as err:
      printInfo(err)
  return None
