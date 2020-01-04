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

  # 赋值时没法区分成员变量和字典值
  # 先判断是否有成员变量
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
