#!/usr/bin/python
#coding=utf-8
class UrlStore:
  _urls=[]
  # _i=0
  _dic=set()
  def popUrl(self):
    url=None
    # if(len(self._urls)>self._i):
    #   url = self._urls[self._i]
    #   self._i = self._i+1
    if(len(self._urls)>0):
      url=self._urls.pop()
    return url
  def getCount(self):
    return len(self._urls)
  def checkUrl(self,url):
    return url in self._dic

  def saveUrl(self, urls):
    if (type(urls).__name__=='dict'):
      urls=urls["Urls"]
    for url in urls:
      if(isinstance(url,str)):
        url={'url':url}
      if(url['url'] not in self._dic):
        self._urls.append(url)
        self._dic.add(url['url'])