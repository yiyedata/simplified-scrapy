#!/usr/bin/python
#coding=utf-8
import time,io,sys,hashlib,os,re
if sys.version_info.major == 2:
  from urlparse import urlparse,urljoin
else:
  from urllib.parse import urlparse,urljoin
def getTime(t):
  return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(t))
def getTimeNow():
  return getTime(time.time())
def convertTime2Str(t):
  return time.strftime('%Y-%m-%d %H:%M:%S', t)
def convertStr2Time(st):
  return time.strptime(st, "%Y-%m-%d %H:%M:%S")
def printInfo(*msgs):
    print(getTime(time.time()),msgs)

# def printError(addr,err):
#   printInfo(addr, err.message)

def saveFile(name,text,encoding="utf-8"):
  file = io.open(name, "w",encoding=encoding)
  try:
    file.write(u'{}\n'.format(text))
  except Exception as err:
    printInfo(err,name)
  file.close()
def getFileContent(name,encoding="utf-8"):
  file = io.open(name, "r",encoding=encoding)
  try:
    return file.read()
  except Exception as err:
    printInfo(err,name)
  finally:
    file.close()
def getFileLines(name,encoding="utf-8"):
  file = io.open(name, "r",encoding=encoding)
  try:
    return file.readlines()
  except Exception as err:
    printInfo(err,name)
  finally:
    file.close()

def getFileInfo(name):
  return os.stat(name)

def getFileModifyTime(name):
  return os.stat(name).st_mtime

def isExistsFile(name):
  return os.path.isfile(name)
def isExistsDir(name):
  return os.path.isdir(name)

def appendFile(name,text,encoding="utf-8"):
  file = io.open(name, "a",encoding=encoding)
  try:
    file.write(u'{}\n'.format(text))
  except Exception as err:
    printInfo(err,name)
  file.close()

def convertUrl2Int(url,count=10):
  value = urlparse(url).netloc
  value = value.split(":")[0]
  myint=0
  for c in value:
    myint += ord(c)
  return myint % count
def md5(text,encoding="utf-8"):
  if sys.version_info.major == 2:
    return hashlib.md5(text).hexdigest()
  else:
    return hashlib.md5(text.encode(encoding)).hexdigest()
def absoluteUrl(baseUrl,url):
  if(not url or url[:7].lower()=="http://" or  url[:8].lower()=="https://"):
    return url
  i = url.find('#')
  if(i>=0):
    url=url[:i]
  if(not url): 
    return baseUrl
  if(urljoin):
    return urljoin(baseUrl,url)
  return urlparse.urljoin(baseUrl,url)
