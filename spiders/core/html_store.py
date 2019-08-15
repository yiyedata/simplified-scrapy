#!/usr/bin/python
#coding=utf-8
import os,io,hashlib
class HtmlStore:
  _htmls=[]
  _htmlPath='htmls/'
  def saveHtml(self,url,html):
    self._htmls.append({"url":url,"html":html})
    if(isinstance(url,str)):
      self._saveHtml(url,html)
    else:
      self._saveHtml(url["url"],html)

  def popHtml(self):
    if(len(self._htmls)>0):
      return self._htmls.pop()

  def _saveHtml(self,url,html):
    filename = hashlib.md5(url).hexdigest()+'.htm'
    if(not os.path.exists(self._htmlPath)):
      os.mkdir(self._htmlPath)
    file = io.open(self._htmlPath+filename, "w",encoding="utf-8")
    file.write(html)
    file.close()
