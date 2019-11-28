#!/usr/bin/python
#coding=utf-8
import simplified_scrapy.core.logex
from simplified_scrapy.core.regex_helper import *

class SimplifiedDoc():
  def __init__(self, html=None,start=None,end=None):
    self.html=None
    self.last=None
    if(not html): return
    sec = getSection(html,start,end)
    if(sec): self.html=html[sec[0]:sec[1]]
    else: self.html=html
  def loadHtml(self,html,start=None,end=None):
    if(not html): return
    sec = getSection(html,start,end)
    if(sec): self.html=html[sec[0]:sec[1]]
    else: self.html=html
  
  def listA(self, html=None, url=None,start=None,end=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return listA(html,url,start,end)

  def listImg(self, html=None, url=None,start=None,end=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return listImg(html,url,start,end)

  def getElementByID(self, id, html=None,start=None,end=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByID(id,html,start,end)
    return self.last

  # def getElementAttrByID(self, id,attr, html=None,start=None,end=None):
  #   if(not html):html=self.html
  #   if(not html and self.last):html=self.last.innerHtml
  #   self.last = getElementAttrByID(id,attr,html,start,end)
  #   return self.last

  def getElementTextByID(self, id, html=None,start=None,end=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return getElementTextByID(id,html,start,end)

  def getElementByTag(self, tag, html=None,start=None,end=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByTag(tag,html,start,end)
    return self.last

  def getElementByClass(self, className, html=None,start=None,end=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByClass(className,html,start,end)
    return self.last

  def getElementsByTag(self, tag, html=None,start=None,end=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return getElementsByTag(tag,html,start,end)

  def getElementsByClass(self, className, html=None,start=None,end=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return getElementsByClass(className,html,start,end)

  def getElementByAttr(self, attr,value, html=None,start=None,end=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByAttr(attr,value,html,start,end)
    return self.last

  def getElement(self,tag,attr='class',value=None, html=None,start=None,end=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElement(tag,attr,value,html,start,end)
    return self.last

  def getElements(self,tag,attr='class',value=None, html=None,start=None,end=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return getElements(tag,attr,value,html,start,end)