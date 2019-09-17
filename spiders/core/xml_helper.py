#!/usr/bin/python
#coding=utf-8
try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET

class XmlDictConfig(dict):
  def __init__(self, parent_element):
    if parent_element.items():
      self.update(dict(parent_element.items()))
      self['text'] = parent_element.text
    
    for element in parent_element:
      if(not self.get(element.tag)):
        self.update({element.tag: []})

      dic = self.getDic(element)
      self[element.tag].append(dic)
      count = len(element)
      if(count>0):
        self.ele2arr(dic,element)
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
def convert2Dic(html):
  try:
    tree = ET.XML(html)
    return XmlDictConfig(tree)
  except Exception as err:
    print err
  return None
# tree = ET.XML('''<list><div id="write-notes-ad" class='asd'><span>12345</span>1<span>12345</span>23</div>
# <div id="write-2" class='asd2'>1232</div><span>asd123</span><span>1234</span></list>''')
# # xmlList = XmlListConfig(tree.items())
# xmldict = XmlDictConfig(tree)
# print xmldict