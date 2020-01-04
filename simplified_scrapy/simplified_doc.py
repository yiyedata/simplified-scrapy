#!/usr/bin/python
#coding=utf-8
import simplified_scrapy.core.logex
from simplified_scrapy.core.regex_helper import *
from simplified_scrapy.core.request_helper import extractHtml
from simplified_scrapy.extracter import ExtractModel
from simplified_scrapy.core.utils import absoluteUrl
from simplified_scrapy.core.regex_dic import RegexDict, RegexDictNew
from simplified_scrapy.core.listex import List
class SimplifiedDoc(RegexDict):
  def __init__(self, html=None,start=None,end=None,before=None):
    # self._rootNode=self
    self['html']=None
    self.last=None
    if(not html): return
    sec = getSection(html,start,end,before)
    if(sec): html=html[sec[0]:sec[1]]
    html = preDealHtml(html)
    self['html'] = html
  def loadHtml(self,html,start=None,end=None,before=None):
    if(not html): return
    sec = getSection(html,start,end,before)
    if(sec): html=html[sec[0]:sec[1]]
    html = preDealHtml(html)
    self['html'] = html
  
  def listA(self, html=None, url=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return listA(html,url,start,end,before)

  def listImg(self, html=None, url=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return listImg(html,url,start,end,before)

  def getElementByID(self, id, html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByID(id,html,start,end,before)
    self.last=RegexDictNew(self.last,root=self)
    return self.last

  def getElementByText(self, text, tag=None, html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByText(text,tag,html,start,end,before)
    self.last=RegexDictNew(self.last,root=self)
    return self.last

  def getElementByReg(self, regex, tag=None, html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByReg(regex,tag,html,start,end,before)
    self.last=RegexDictNew(self.last,root=self)
    return self.last

  def getElementByTag(self, tag, html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByTag(tag,html,start,end,before)
    self.last=RegexDictNew(self.last,root=self)
    return self.last

  def getElementByClass(self, className, html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByClass(className,html,start,end,before)
    self.last=RegexDictNew(self.last,root=self)
    return self.last
  def _convert2lst(self,eles):
    lst=List()
    if(eles):
      for e in eles:
        dic=RegexDictNew(e,root=self)
        lst.append(dic)
    return lst
  def getElementsByTag(self, tag, html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    eles = getElementsByTag(tag,html,start,end,before)
    return self._convert2lst(eles)

  def getElementsByClass(self, className, html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    eles =  getElementsByClass(className,html,start,end,before)
    return self._convert2lst(eles)

  def getElementByAttr(self, attr,value, html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByAttr(attr,value,html,start,end,before)
    self.last=RegexDictNew(self.last,root=self)
    return self.last

  def getElement(self,tag,attr='class',value=None, html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElement(tag,attr,value,html,start,end,before)
    self.last=RegexDictNew(self.last,root=self)
    return self.last

  def removeElement(self,tag,attr='class',value=None, html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self['html']= removeElement(tag,attr,value,html,start,end,before)
    return self['html']

  def getElements(self,tag,attr='class',value=None, html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    eles = getElements(tag,attr,value,html,start,end,before)
    return self._convert2lst(eles)

  def getParent(self,tag=None,attr=None,value=None,html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getParent(tag,attr,value,html,start,end,before)
    self.last=RegexDictNew(self.last,root=self)
    return self.last
    
  def getChildren(self,html=None,tag=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    eles = getChildren(html,tag,start,end,before)
    return self._convert2lst(eles)

  def getNexts(self,attr,value,html,tag=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    eles = getNexts(attr,value,html,tag,start,end,before)
    return self._convert2lst(eles)
  def getElementByStr(self,html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    s,e=getSection(html,start,end,before)
    if s<0 or e<0: 
      return None
    if end: e+=len(end)
    ele = Dict()
    ele.html = html[s:e]
    ele._start = s
    ele._end = e
    return ele
  def getElementsByStr(self,html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    lst = []
    ele = None
    while True:
      s=0
      if ele: s=ele._end
      h = html[s:]
      ele = self.getElementByStr(h,start,end,before)
      if(not ele): break
      ele._start += s
      ele._end += s
      lst.append(ele)
    return lst
    
  def getSection(self,html=None,start=None,end=None,before=None):
    return self._getSection(html,start,end,before)[0]

  def _getSection(self,html=None,start=None,end=None,before=None):
    if html: html = preDealHtml(html)
    if(not html): html=self.html
    if(not html and self.last):html=self.last.innerHtml
    s,e=getSection(html,start,end,before)
    l = 0
    if before: l=len(before)
    elif start: l=len(start)
    el=0
    if end: el=len(end)
    if s<0: 
      s=0
      l=0
    if e<0: 
      e=len(html)
      el=0
    return (html[s+l:e],s,e+el)
    
  def removeHtml(self,html,replace=''):
    return removeHtml(html,replace)

  def trimHtml(self,html):
    return trimHtml(html)

  def replaceReg(self,html,regex,new):
    return replaceReg(html,regex,new)

  def absoluteUrl(self,baseUrl,url):
    return absoluteUrl(baseUrl,url)

  def getObjByModel(self,html,url=None,models=[{"Type":3}],title=None):
    if(not isinstance(models,dict) and not isinstance(models,list)):
      models = json.loads(models)
    if(isinstance(models,dict)):
      models = [models]
    return extractHtml(url,html,models,None,title)