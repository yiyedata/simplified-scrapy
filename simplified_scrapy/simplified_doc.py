#!/usr/bin/python
#coding=utf-8
from simplified_scrapy.core.regex_helper import *
  
class SimplifiedDoc():
  def __init__(self, html=None,start=None,end=None):
    sec = getSection(html,start,end)
    if(sec): self.html=html[sec[0]:sec[1]]
    else: self.html=html
  def loadHtml(self,html,start=None,end=None):
    sec = getSection(html,start,end)
    if(sec): self.html=html[sec[0]:sec[1]]
    else: self.html=html
  
  def listA(self, html=None, url=None,start=None,end=None):
    if(not html):html=self.html
    return listA(html,url,start,end)

  def listImg(self, html=None, url=None,start=None,end=None):
    if(not html):html=self.html
    return listImg(html,url,start,end)

  def getElementByID(self, id, html=None,start=None,end=None):
    if(not html):html=self.html
    return getElementByID(id,html,start,end)

  def getElementAttrByID(self, id,attr, html=None,start=None,end=None):
    if(not html):html=self.html
    return getElementAttrByID(id,attr,html,start,end)

  def getElementTextByID(self, id, html=None,start=None,end=None):
    if(not html):html=self.html
    return getElementTextByID(id,html,start,end)

  def getElementByTag(self, tag, html=None,start=None,end=None):
    if(not html):html=self.html
    return getElementByTag(tag,html,start,end)

  def getElementByClass(self, className, html=None,start=None,end=None):
    if(not html):html=self.html
    return getElementByClass(className,html,start,end)

  def getElementsByTag(self, tag, html=None,start=None,end=None):
    if(not html):html=self.html
    return getElementsByTag(tag,html,start,end)

  def getElementsByClass(self, className, html=None,start=None,end=None):
    if(not html):html=self.html
    return getElementsByClass(className,html,start,end)

  def getElementByAttr(self, attr,value, html=None,start=None,end=None):
    if(not html):html=self.html
    return getElementByAttr(attr,value,html,start,end)

  def getElement(self,tag,attr='class',value=None, html=None,start=None,end=None):
    if(not html):html=self.html
    return getElement(tag,attr,value,html,start,end)

  def getElements(self,tag,attr='class',value=None, html=None,start=None,end=None):
    if(not html):html=self.html
    return getElements(tag,attr,value,html,start,end)