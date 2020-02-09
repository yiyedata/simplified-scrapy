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
      if attr=='outerHtml':
        if self._rootNode:
          return self._rootNode.html[self._start:self._end]
      # if attr=='innerHtml':
      #   return self.get('html')
      if attr=='text':# or attr=='innerText':
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
        html = self.get('html')
        if html and html.find('<'+attr+' ')<0 and html.find('<'+attr+'>')<0:
          return self.getElementsByTag(attr[:-1])
      return self.getElementByTag(attr)
  def unescape(self,text=None):
    if not text:
      text = self.text
    if text:
      return HTMLParser().unescape(text)
    return ""
    
  def listA(self, url=None,start=None,end=None,before=None):
    if(not self.html): return List()
    return List(listA(self.html,url,start,end,before))

  def listImg(self, url=None,start=None,end=None,before=None):
    if(not self.html): return List()
    return List(listImg(self.html,url,start,end,before))

  def getElementByID(self, id,start=None,end=None,before=None):
    if(not self.html): return Dict()
    ele = getElementByID(id,self.html,start,end,before)
    return RegexDictNew(ele,root=self._rootNode,parent=self)

  def getElementByTag(self, tag,start=None,end=None,before=None):
    if(not self.html): return Dict()
    ele = getElementByTag(tag,self.html,start,end,before)
    return RegexDictNew(ele,root=self._rootNode,parent=self)

  def getElementByClass(self, className,start=None,end=None,before=None):
    if(not self.html): return Dict()
    ele = getElementByClass(className,self.html,start,end,before)
    return RegexDictNew(ele,root=self._rootNode,parent=self)

  def getElementsByTag(self, tag,start=None,end=None,before=None):
    if(not self.html): return List()
    eles = getElementsByTag(tag,self.html,start,end,before)
    return self._convert2lst(eles,parent=self)

  def getElementsByClass(self, className,start=None,end=None,before=None):
    if(not self.html): return List()
    eles = getElementsByClass(className,self.html,start,end,before)
    return self._convert2lst(eles,parent=self)

  def getElementByAttr(self, attr,value,start=None,end=None,before=None):
    if(not self.html): return Dict()
    ele = getElementByAttr(attr,value,self.html,start,end,before)
    return RegexDictNew(ele,root=self._rootNode,parent=self)

  def getElement(self,tag,attr='class',value=None,start=None,end=None,before=None):
    if(not self.html): return Dict()
    ele = getElement(tag,attr,value,self.html,start,end,before)
    return RegexDictNew(ele,root=self._rootNode,parent=self)

  def removeElement(self,tag,attr='class',value=None,start=None,end=None,before=None):
     if(self.html): 
      self['html'] = removeElement(tag,attr,value,self.html,start,end,before)
     return self

  def getElements(self,tag,attr='class',value=None,start=None,end=None,before=None):
    if(not self.html): return List()
    eles = getElements(tag,attr,value,self.html,start,end,before)
    return self._convert2lst(eles,self)

  def getElementByText(self, text, tag=None,start=None,end=None,before=None):
    if(not self.html): return Dict()
    ele = getElementByText(text, tag, self.html,start,end,before)
    return RegexDictNew(ele,root=self._rootNode,parent=self)
    
  def getElementByReg(self, regex, tag=None,start=None,end=None,before=None):
    if(not self.html): return Dict()
    ele = getElementByReg(regex, tag,self.html,start,end,before)
    return RegexDictNew(ele,root=self._rootNode,parent=self)
    
  def getParent(self,tag=None):
    if(not self._rootNode): return Dict()
    html=self._rootNode.html
    ele = getParent4Ele(html,self,tag)
    return RegexDictNew(ele,root=self._rootNode)
  def getNexts(self,tag=None):
    if(not self._rootNode): return List()
    html = self._rootNode.html
    eles = getNexts4Ele(html,self,tag)
    return self._convert2lst(eles,s=self._end)
  def getPrevious(self,tag=None):
    if(not self._rootNode): return List()
    html = self._rootNode.html
    eles = getPrevious4Ele(html,self,tag)
    return self._convert2lst(eles)

  def getNext(self,tag=None):
    if(not self._rootNode): return Dict()
    html = self._rootNode.html
    eles = getNext4Ele(html,self,tag)
    return RegexDictNew(eles,root=self._rootNode,s=0)#self._end)

  def getChild(self,tag=None,start=None,end=None,before=None):
    if(not self.html): return None
    eles = getChild(self.html,tag,start,end,before)
    s=self._rootNode.html.find('>',self._start)+1
    return RegexDictNew(eles,root=self._rootNode,s=s)
  def getChildren(self,tag=None,start=None,end=None,before=None):
    if(not self.html): return List()
    eles = getChildren(self.html,tag,start,end,before)
    s=self._rootNode.html.find('>',self._start)+1
    return self._convert2lst(eles,s=s)
  def getText(self,separator='',tags=None):
    return removeHtml(self.get('html'),separator,tags)
  def nextText(self):
    if not self._rootNode or not self._rootNode.html:
      return ''
    start = self._end
    s = start
    html = self._rootNode.html
    while True:
      end = html.find('<',s)
      r = html.find('>',s)
      if end<0 or r<0:
        return html[start:].strip()
      m = html[end+1:r].find('<')
      if m<0:
        return html[start:end].strip()
      s += m
  def previousText(self):
    if not self._rootNode or not self._rootNode.html:
      return ''
    end = self._start
    s = end
    html = self._rootNode.html
    while True:
      s = html.rfind('>',0,s)
      r = html.rfind('<',0,s)
      if s<0 or r<0:
        return html[0:end].strip()
      m = html[r:s].find('>')
      if m<0:
        return html[s+1:end].strip()
      return html[r+m+1:end].strip()
  def firstText(self):
    if not self.html:
      return ''
    start = 0
    s = start
    html = self.html
    while True:
      end = html.find('<',s)
      r = html.find('>',s)
      if end<0 or r<0:
        return html[start:].strip()
      m = html[end+1:r].find('<')
      if m<0:
        return html[start:end].strip()
      s += m
  def trimHtml(self):
    if(not self.html): return None
    self['html'] = trimHtml(self.html)
    return self.html

  # def contains(self, value, attr='html'):
  #   if(self[attr]==None): return False
  #   if isinstance(value, list):
  #     for r in value:
  #       if self[attr].find(r)<0:
  #         return False
  #   else:
  #     if value and self[attr].find(value)<0:
  #       return False
  #   return True
  # def containsOr(self, value, attr='html'):
  #   if(self[attr]==None): return False
  #   if isinstance(value, list):
  #     for r in value:
  #       if self[attr].find(r)>=0:
  #         return True
  #     return False
  #   else:
  #     if value and self[attr].find(value)<0:
  #       return False
  #   return True

  # def notContains(self, value, attr='html'):
  #   if(self[attr]==None): return True
  #   if isinstance(value, list):
  #     for r in value:
  #       if self[attr].find(r)>=0:
  #         return False
  #   else:
  #     if not value or self[attr].find(value)>=0:
  #       return False
  #   return True
    
  # def containsReg(self, value, attr='html'):
  #   if(not self[attr]): return False
  #   return checkContains(self[attr], value)

  def _convert2lst(self,eles,parent=None,s=None):
    lst=List()
    if(eles):
      for e in eles:
        lst.append(RegexDictNew(e,root=self._rootNode,parent=parent,s=s))
    return lst
  def replaceReg(self,regex,new):
    if self.html:
      self['html']=replaceReg(self.html,regex,new)
    return self.html
  def getSectionByReg(self,regex,group=0,start=None,end=None,before=None):
    return getOneByReg(self.html,regex,group,start,end,before)

  def getSectionsByReg(self,regex,group=0,start=None,end=None,before=None):
    return getListByReg(self.html,regex,group,start,end,before)
  def select(self,value,start=None,end=None,before=None):
    return _select(self,value,start,end,before)
  def selects(self,value,start=None,end=None,before=None):
    if value == None: return List()
    s = value.find('(')
    tp = None
    if s>0:
      s = value.rfind('>',0,s)
      if s>0:
        tp = value[s+1:]
        value = value[0:s]
      else:
        tp = value
        value=''
    values = value.split('>')
    N = len(values)
    ele=None
    _ele=self
    for i in range(0,N-1):
      v = values[i]
      if not v: continue
      tag,attr,value = _getParas(v.strip())
      ele = _ele.getElement(tag,attr,value,start=start,end=end,before=before)
      _ele = ele
      if not _ele:
        return List()
    tag,attr,value = _getParas(values[N-1])
    eles = _ele.getElements(tag,attr,value,start=start,end=end,before=before)
    start = end = before = None
    if tp:
      eles = [_selectText(e,tp) for e in eles]
    return eles
def _getValue(_ele,attr):
  return _ele.__getattr__(attr)
  # if attr in ['text','innerText']: return _ele.text
  # elif attr in ['innerHtml']: return _ele.html
  # else: 
  #   return _ele[attr]
def _select(_self,value,start=None,end=None,before=None):
  if value == None: return None
  s = value.find('(')
  tp = None
  if s>0:
    s = value.rfind('>',0,s)
    if s>0:
      tp = value[s+1:]
      value = value[0:s]
    else:
      tp = value
      value=''
  values = value.split('>')
  ele=None
  _ele=_self
  for v in values:
    if not v: continue
    tag,attr,value = _getParas(v.strip())
    ele = _ele.getElement(tag,attr,value,start=start,end=end,before=before)
    start = end = before = None
    _ele = ele
    if not _ele:
      return None
  if tp:
    return _selectText(_ele,tp,start,end,before)
  return ele
def _selectText(_ele,value,start=None,end=None,before=None):
  v = value.strip()
  obj = []
  s = 0
  while True:
    index = v.find('(',s)
    if index<0:
      break
    _attr = v[s:index]
    if not _attr: _attr='text'
    e = v.find(')',index)
    t = v.find('(',index+1)
    if t>index and t<e:
      s = index+1
      continue
    p = v[index+1:e].strip()
    if not p:
      if _attr.find('>')<0:
        obj.append(_getValue(_ele,_attr))
      else:
        objs=_select(_ele,_attr+'()')
        if isinstance(objs, list):
          for o in objs: obj.append(o)
        else:
          obj.append(objs)
    else:
      paras = p.split(',')
      if len(paras)==1:
        tag,attr,value = _getParas(paras[0].strip())
        ele = _ele.getElement(tag,attr,value,start=start,end=end,before=before)
        if ele: obj.append(_getValue(ele,_attr))
        else: obj.append(None)
      else:
        for para in paras:
          tag,attr,value = _getParas(para.strip())
          ele = _ele.getElement(tag,attr,value,start=start,end=end,before=before)
          start = end = before = None
          obj.append(_getValue(ele,_attr) if ele else None)
    
    s = v.find(',',e)+1
    if s==0: break
  if len(obj)==1: return obj[0]
  return obj
def _getParas(value):
  paras = re.split("(\.|#|@)",value)
  if not paras[0]: del paras[0]
  tag=None
  attr=None
  value=None
  N=len(paras)-1
  i=0
  while i<N:
    para = paras[i]
    if para=='.':
      attr='class'
      value=paras[i+1]
    if para=='#':
      attr='id'
      value=paras[i+1]
    if para=='@':
      kv = paras[i+1].split('=')
      attr=kv[0].strip()
      value=kv[1].strip('\'" ')
    else:
      i+=1
      continue
    i+=1
  if N==0 or '.#@'.find(paras[0])<0:
    tag=paras[0]
  return tag.split('|') if tag else None,attr,value
def RegexDictNew(dic,root,parent=None,s=None):
  if not dic: return Dict()
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
# def convert2rdicLst(lst):
#   eles = List()
#   for l in lst:
#     eles.append(RegexDict(l))
#   return eles