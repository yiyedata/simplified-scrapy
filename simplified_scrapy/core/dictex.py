#!/usr/bin/python
#coding=utf-8

class Dict(dict):
  def __getattr__(self,attr):
    if(self.get(attr)):
      return self.get(attr)
    else:
      return None

  def __getitem__(self,attr):
    if(self.get(attr)):
      return self.get(attr)
    else:
      return None
      
  def set(self,key,value):
    self[key]=value