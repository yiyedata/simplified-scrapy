#!/usr/bin/python
#coding=utf-8
class HtmlStoreBase:
  def saveHtml(self,url,html):
    raise NotImplementedError

  def popHtml(self,state=0):
    raise NotImplementedError

  def updateState(self,id,state):
    raise NotImplementedError