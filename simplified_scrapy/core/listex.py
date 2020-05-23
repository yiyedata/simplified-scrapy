#!/usr/bin/python
#coding=utf-8
class List(list):
  def __getattr__(self,attr):
    tmp = List()
    for l in self:
      tmp.append(l.__getattr__(attr))
    return tmp

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

# class List(_List):
  def nextText(self, end=None):
    tmp = List()
    for l in self:
      tmp.append(l.nextText(end))
    return tmp
  def previousText(self):
    tmp = List()
    for l in self:
      tmp.append(l.previousText())
    return tmp
  def select(self,value,start=None,end=None,before=None):
    tmp = List()
    for l in self:
      tmp.append(l.select(value,start,end,before))
    return tmp
  def selects(self,value,start=None,end=None,before=None):
    tmp = List()
    for l in self:
      tmp.append(l.selects(value,start,end,before))
    return tmp
  def getElement(self,tag,attr='class',value=None,start=None,end=None,before=None):
    tmp = List()
    for l in self:
      tmp.append(l.getElement(tag,attr,value,start,end,before))
    return tmp
  def getElements(self,tag,attr='class',value=None,start=None,end=None,before=None):
    tmp = List()
    for l in self:
      tmp.append(l.getElements(tag,attr,value,start,end,before))
    return tmp
  def getTable(self,body='tbody',columns=None,rowReg=None,colReg=None,start=None,end=None,before=None):
    tmp = List()
    for l in self:
      tmp.append(l.getTable(body,columns,rowReg,colReg,start=start,end=end,before=before))
    return tmp
  def getNext(self,tag=None):
    tmp = List()
    for l in self:
      tmp.append(l.getNext(tag))
    return tmp