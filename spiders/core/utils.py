#!/usr/bin/python
#coding=utf-8
import time,io
def getTime(t):
  return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(t))
def getTimeNow():
  return getTime(time.time())

def printInfo(*msgs):
  print getTime(time.time())
  print msgs

# def printError(addr,err):
#   printInfo(addr, err.message)

def saveFile(name,text):
  file = io.open(name, "w",encoding="utf-8")
  try:
    file.write(u'{}\n'.format(text))
  except Exception as err:
    printInfo(err,name)
  file.close()

def appendFile(name,text):
  file = io.open(name, "a",encoding="utf-8")
  try:
    file.write(u'{}\n'.format(text))
  except Exception as err:
    printInfo(err,name)
  file.close()