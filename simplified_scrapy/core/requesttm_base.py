#!/usr/bin/python
#coding=utf-8
class RequestTmBase:
  def addRecode(self, ssp, url, tmSpan, state, concurrency,countPer10s,size):
    raise NotImplementedError

  def startRecode(self):
    raise NotImplementedError
  def startServer(self):
    raise NotImplementedError
  def endRecode(self):
    raise NotImplementedError