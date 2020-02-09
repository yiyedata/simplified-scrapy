#!/usr/bin/python
#coding=utf-8
class List(list):
  def equal(self, value, attr='class'):
    tmp=List()
    for l in self:
      if hasattr(l, 'equal'):
        flag = l.equal(value,attr)
        if flag: tmp.append(l)
    return tmp
  def contains(self, value, attr='html'):
    tmp=List()
    for l in self:
      if hasattr(l, 'contains'):
        flag = l.contains(value,attr)
        if flag: tmp.append(l)
    return tmp
  def containsOr(self, value, attr='html'):
    tmp=List()
    for l in self:
      if hasattr(l, 'containsOr'):
        flag = l.containsOr(value,attr)
        if flag: tmp.append(l)
    return tmp
  def notContains(self, value, attr='html'):
    tmp=List()
    for l in self:
      if hasattr(l, 'notContains'):
        flag = l.notContains(value,attr)
        if flag: tmp.append(l)
    return tmp

  def containsReg(self, value, attr='html'):
    tmp=[]
    for l in self:
      if hasattr(l, 'containsReg'):
        flag = l.containsReg(value,attr)
        if not flag: tmp.append(l)
    for t in tmp:
      self.remove(t)
    return self

  
