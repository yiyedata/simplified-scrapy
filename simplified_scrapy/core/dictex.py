#!/usr/bin/python
#coding=utf-8

class Dict(dict):
  _start=None
  _end=None
  def __getattr__(self,attr):
    if(self.get(attr)):
      return self.get(attr)
    else:
      return None

  # def __setattr__(self, key, value):
  #   self[key] = value

  def __getitem__(self,attr):
    if(self.get(attr)):
      return self.get(attr)
    else:
      return None
  def __delattr__(self,key):
    del self[key]
  # def set(self,key,value):
  #   self[key]=value

  def equal(self, value, attr='class'):
    v = self.__getattr__(attr)
    if(v==None): return False
    if isinstance(value, list):
      for r in value:
        if v==r:
          return True
    else:
      return v==value
    return False
  def contains(self, value, attr='html'):
    v = self.__getattr__(attr)
    if(v==None): return False
    if isinstance(value, list):
      for r in value:
        if v.find(r)<0:
          return False
    else:
      if value and v.find(value)<0:
        return False
    return True
  def containsOr(self, value, attr='html'):
    v = self.__getattr__(attr)
    if(v==None): return False
    if isinstance(value, list):
      for r in value:
        if v.find(r)>=0:
          return True
      return False
    else:
      if value and v.find(value)<0:
        return False
    return True

  def notContains(self, value, attr='html'):
    v = self.__getattr__(attr)
    if(v==None): return True
    if isinstance(value, list):
      for r in value:
        if v.find(r)>=0:
          return False
    else:
      if not value or v.find(value)>=0:
        return False
    return True
    
  def containsReg(self, value, attr='html'):
    v = self.__getattr__(attr)
    if(not v): return False
    return _checkContains(v, value)
def _checkContains(html, reg):
  import re
  return not not re.compile(reg).search(html)