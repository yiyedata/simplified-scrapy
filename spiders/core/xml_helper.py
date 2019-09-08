#!/usr/bin/python
#coding=utf-8
try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET
# class XmlListConfig(list):
#   def __init__(self, aList):
#     for element in aList:
#       if element:
#         if len(element) == 1 or element[0].tag != element[1].tag:
#           self.append(XmlDictConfig(element))
#         elif element[0].tag == element[1].tag:
#           self.append(XmlListConfig(element))
#       elif element.text:
#         text = element.text.strip()
#         if text:
#           self.append(text)

class XmlDictConfig(dict):
  def __init__(self, parent_element):
    if parent_element.items():
      self.update(dict(parent_element.items()))
      self['text'] = parent_element.text

    count = len(parent_element)
    
    for element in parent_element:
      if element:
        if len(element) == 1 or element[0].tag != element[1].tag:
          aDict = XmlDictConfig(element)
        else:
          # aDict = {element[0].tag: XmlListConfig(element)}
          aDict={}
          self.ele2arr(aDict, element)
          print element
        if element.items():
          aDict.update(dict(element.items()))
          aDict['text'] = element.text
        if(count>1):
          if(not self.get(element.tag)):
            self.update({element.tag: []})
          self[element.tag].append(aDict)
        else:
          self.update({element.tag: aDict})
      elif element.items():
        if(count>1):
          if(not self.get(element.tag)):
            self.update({element.tag: []})
          dic = dict(element.items())
          dic['text'] = element.text
          self[element.tag].append(dic)
        else:
          dic = dict(element.items())
          dic['text'] = element.text
          self.update({element.tag: dic})
      else:
        self.update({element.tag: element.text})

  def ele2arr(self,dic,elements):
    pass

tree = ET.XML('''<list><div id="write-notes-ad" class='asd'>123</div>
<div id="write-2" class='asd2'>1232</div></list>''')
# xmlList = XmlListConfig(tree.items())
xmldict = XmlDictConfig(tree)
print xmldict