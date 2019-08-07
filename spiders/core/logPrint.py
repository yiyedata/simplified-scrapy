#!/usr/bin/python
#coding=utf-8
import time,io
import logging,traceback
logging.basicConfig(
  level=logging.DEBUG,#控制台打印的日志级别
  filename='spider.log',
  filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志。a是追加模式，默认如果不写的话，就是追加模式
  format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

def getTime(t):
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(t))
def logPrint(*msgs):
  print getTime(time.time())
  print msgs

def printTxt(*msgs):
  print msgs

def logError(addr,*msgs):
  logging.error(addr)
  for msg in msgs:
    logging.error(msg)
  print addr, msgs
def saveFile(name,text):
    file = io.open(name, "w",encoding="utf-8")
    file.write(u'{}\n'.format(text))
    file.close()
def appendFile(name,text):
    file = io.open(name, "a",encoding="utf-8")
    file.write(u'{}\n'.format(text))
    file.close()
# logError('test')