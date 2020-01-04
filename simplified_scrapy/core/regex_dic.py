import simplified_scrapy.core.logex
from simplified_scrapy.core.regex_helper import *
from simplified_scrapy.core.request_helper import extractHtml
from simplified_scrapy.extracter import ExtractModel
from simplified_scrapy.core.utils import absoluteUrl
from simplified_scrapy.core.dictex import Dict
from simplified_scrapy.core.listex import List
try: 
  from HTMLParser import HTMLParser
except ImportError:
  from html.parser import HTMLParser
class RegexDict(Dict):
  _rootNode = None
  _parentNode = None
  def __getattr__(self,attr):
    if not attr: return None
    if(self.get(attr) != None):
      return self.get(attr)
    elif attr=='html':
      return ''
    else:
      if attr=='innerHtml':
        return self.get('html')
      if attr=='innerText' or attr=='text':
        return removeHtml(self.get('html'))
      if attr=='children':
        return self.getChildren()
      if attr=='child':
        return self.getChild()
      if attr=='nexts':
        return self.getNexts()
      if attr=='next':
        return self.getNext()
      if attr=='previous':
        return self.getPrevious()
      if attr=='parent':
        return self.getParent()
      if len(attr)>1 and attr[-1:] == 's':
        return self.getElementsByTag(attr[:-1])
      return self.getElementByTag(attr)
  def unescape(self,text=None):
    if not text:
      text = self.text
    if text:
      return HTMLParser().unescape(text)
    return ""
    
  def listA(self, url=None,start=None,end=None,before=None):
    if(not self.html): return None
    return listA(self.html,url,start,end,before)

  def listImg(self, url=None,start=None,end=None,before=None):
    if(not self.html): return None
    return listImg(self.html,url,start,end,before)

  def getElementByID(self, id,start=None,end=None,before=None):
    if(not self.html): return None
    ele = getElementByID(id,self.html,start,end,before)
    if(ele):
      return RegexDictNew(ele,root=self._rootNode,parent=self)
    return None

  def getElementByTag(self, tag,start=None,end=None,before=None):
    if(not self.html): return None
    ele = getElementByTag(tag,self.html,start,end,before)
    if(ele):
      return RegexDictNew(ele,root=self._rootNode,parent=self)
    return None

  def getElementByClass(self, className,start=None,end=None,before=None):
    if(not self.html): return None
    ele = getElementByClass(className,self.html,start,end,before)
    if(ele):
      return RegexDictNew(ele,root=self._rootNode,parent=self)
    return None

  def getElementsByTag(self, tag,start=None,end=None,before=None):
    if(not self.html): return None
    eles = getElementsByTag(tag,self.html,start,end,before)
    return self._convert2lst(eles,parent=self)

  def getElementsByClass(self, className,start=None,end=None,before=None):
    if(not self.html): return None
    eles = getElementsByClass(className,self.html,start,end,before)
    return self._convert2lst(eles,parent=self)

  def getElementByAttr(self, attr,value,start=None,end=None,before=None):
    if(not self.html): return None
    ele = getElementByAttr(attr,value,self.html,start,end,before)
    if(ele):
      return RegexDictNew(ele,root=self._rootNode,parent=self)
    return None

  def getElement(self,tag,attr='class',value=None,start=None,end=None,before=None):
    if(not self.html): return None
    ele = getElement(tag,attr,value,self.html,start,end,before)
    if(ele):
      return RegexDictNew(ele,root=self._rootNode,parent=self)
    return None

  def removeElement(self,tag,attr='class',value=None,start=None,end=None,before=None):
     if(self.html): 
      self['html'] = removeElement(tag,attr,value,self.html,start,end,before)
     return self

  def getElements(self,tag,attr='class',value=None,start=None,end=None,before=None):
    if(not self.html): return None
    eles = getElements(tag,attr,value,self.html,start,end,before)
    return self._convert2lst(eles,self)

  def getElementByText(self, text, tag=None,start=None,end=None,before=None):
    html=self.html
    ele = getElementByText(text, tag, html,start,end,before)
    if(ele):
      return RegexDictNew(ele,root=self._rootNode,parent=self)
    return None
  def getElementByReg(self, regex, tag=None,start=None,end=None,before=None):
    html=self.html
    ele = getElementByReg(regex, tag, html,start,end,before)
    if(ele):
      return RegexDictNew(ele,root=self._rootNode,parent=self)
    return None
  def getParent(self,tag=None):
    html=self._rootNode.html
    ele = getParent4Ele(html,self,tag)
    return RegexDictNew(ele,root=self._rootNode)
  def getNexts(self,tag=None):
    html = self._rootNode.html
    eles = getNexts4Ele(html,self,tag)
    return self._convert2lst(eles,s=self._end)
  def getPrevious(self,tag=None):
    html = self._rootNode.html
    eles = getPrevious4Ele(html,self,tag)
    return self._convert2lst(eles)

  def getNext(self,tag=None):
    html = self._rootNode.html
    eles = getNext4Ele(html,self,tag)
    return RegexDictNew(eles,root=self._rootNode,s=0)#self._end)

  def getChild(self,tag=None,start=None,end=None,before=None):
    if(not self.html): return None
    eles = getChild(self.html,tag,start,end,before)
    s=self._rootNode.html.find('>',self._start)+1
    return RegexDictNew(eles,root=self._rootNode,s=s)
  def getChildren(self,tag=None,start=None,end=None,before=None):
    if(not self.html): return None
    eles = getChildren(self.html,tag,start,end,before)
    s=self._rootNode.html.find('>',self._start)+1
    return self._convert2lst(eles,s=s)
  def getText(self,separator=''):
    return removeHtml(self.get('html'),separator)
    
  def trimHtml(self):
    if(not self.html): return None
    self['html'] = trimHtml(self.html)
    return self.html

  def contains(self, value, attr='html'):
    if(self[attr]==None): return False
    if isinstance(value, list):
      for r in value:
        if self[attr].find(r)<0:
          return False
    else:
      if value and self[attr].find(value)<0:
        return False
    return True

  def notContains(self, value, attr='html'):
    if(self[attr]==None): return True
    if isinstance(value, list):
      for r in value:
        if self[attr].find(r)>=0:
          return False
    else:
      if not value or self[attr].find(value)>=0:
        return False
    return True
    
  def containsReg(self, value, attr='html'):
    if(not self[attr]): return False
    return checkContains(self[attr], value)

  def _convert2lst(self,eles,parent=None,s=None):
    lst=List()
    if(eles):
      for e in eles:
        lst.append(RegexDictNew(e,root=self._rootNode,parent=parent,s=s))
    return lst

def RegexDictNew(dic,root,parent=None,s=None):
  if not dic: return None
  ele = RegexDict(dic)
  _s=0
  if s!=None: _s=s
  elif parent: 
    _s=root.html.find('>',parent._start)+1
  ele._start=dic._start+_s
  ele._end=dic._end+_s
  ele._rootNode=root
  ele._parentNode=parent
  return ele