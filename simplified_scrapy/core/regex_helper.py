#!/usr/bin/python
#coding=utf-8
import re,json
import sys
from simplified_scrapy.core.utils import printInfo,absoluteUrl,md5
from simplified_scrapy.core.xml_helper import XmlDictConfig,convert2Dic
from simplified_scrapy.core.dictex import Dict

def getSection(html,start=None,end=None,before=None):
  s = 0
  e = len(html)
  if(start): 
    if(isinstance(start,int)): s=start
    else: s=html.find(start)
  if(end): 
    if(isinstance(end,int)): e=end
    else: e=html.find(end,s)
  if(before):
    if(isinstance(before,int)): s=before
    else: s=html.rfind(before,0,end)
  return (s,e)
def listA(html,baseUrl=None,start=None,end=None,before=None):
  if(not html): return []
  section = getSection(html,start,end,before)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return []
  html = html[s:e]
  if(not html or html.find("<a")<0): return []

  patternLst = re.compile(u'<a[\s]+[^>]*>[\s\S]*?</a>')
  patternUrl = re.compile(u'href[\s=]+[\'"](?P<url>.*?)[\'"]') 
  patternTitle1 = re.compile(u'title[\s=]+[\'"](?P<title>.*?)[\'"]')
  patternTitle2 = re.compile(u'<a[^>]*>(?P<title>.*?)</a>')

  strA = patternLst.findall(html)
  lst=[]
  for i in strA:
    url = None
    title = None
    tmp = patternUrl.search(i)
    if tmp: url = tmp.group("url")
      
    tmp = patternTitle1.search(i)
    if tmp: title = tmp.group("title")
    if(not title):
      tmp = patternTitle2.search(i)
      if tmp: 
        title = tmp.group("title")
        title = re.compile('<[\s\S]*?>').sub('',title)

    try:
      if(url):
        url = url.strip()
        if(baseUrl and url[:7].lower()!="http://" and  url[:8].lower()!="https://"):
          absUrl = absoluteUrl(baseUrl,url)
          if(absUrl!=url):
            lst.append({'url':absUrl,'title':title,'relativeUrl':url})
        else:
          lst.append({'url':url,'title':title})
    except Exception as ex:
      printInfo(ex)
    
  return lst
def listImg(html,baseUrl=None,start=None,end=None,before=None):
  if(not html or html.find("<img")<0): return []
  section = getSection(html,start,end,before)
  s = section[0]
  e = section[1]

  if(s < 0 or e < s): return None
  html = html[s:e]
  if(not html or html.find("<img")<0): return None

  patternLst = re.compile(u'<img[\s]+[^>]*>')
  patternUrl = re.compile(u'src[\s=]+[\'"](?P<url>.*?)[\'"]') 
  patternTitle = re.compile(u'alt[\s=]+[\'"](?P<title>.*?)[\'"]')
  lstStr = patternLst.findall(html)
  lst=[]
  for i in lstStr:
    url = None
    title = None
    tmp = patternUrl.search(i)
    if tmp: 
      url = tmp.group("url")
      
    tmp = patternTitle.search(i)
    if tmp:
      title = tmp.group("title")
    try:
      if(url):
        if(baseUrl and url[:7].lower()!="http://" and  url[:8].lower()!="https://"):
          absUrl = absoluteUrl(baseUrl,url)
          if(absUrl!=url):
            lst.append({'url':absUrl,'alt':title, 'relativeUrl':url})
        else:
          lst.append({'url':url,'alt':title})
    except Exception as ex:
      printInfo(ex)
    
  return lst

def getElementsByTag(tag,html,start=None,end=None,before=None):
  lst=[]
  section = getSection(html,start,end,before)
  if(section[1]<=section[0]):
    return lst
  h=html[section[0]:section[1]]
  s=0
  while True:
    obj = _getElementByTag(tag,h,s)
    if(obj and obj[0] and obj[2]>0):
      lst.append(obj[0])
      s+=obj[2]
    else:
      break
  return lst

def getElementByTag(tag,html,start=None,end=None,before=None):
  obj = _getElementByTag(tag,html,start,end,before)
  if(obj and obj[0]):
    return obj[0]
  return None
def _checkSingleTag(tag):
  tags = ['br','hr','img','input','param','meta','link']
  return tag.lower() in tags
def _getElementByTag(tag,html,start=None,end=None,before=None):
  if(not tag or not html or html.find(tag)<0): return None
  section = getSection(html,start,end,before)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return None

  html = html[s:e]
  if(not html): return None
  singleTag = _checkSingleTag(tag)
  if(singleTag):
    pattern = re.compile(u'<'+tag+'[^>]*?>') 
  else:
    pattern = re.compile(u'<[\s]*'+tag+'[^>]*?>[\s\S]*?</'+tag+'>') 
  m = pattern.search(html)
  if m: 
    dom = m.group(0)
    start = html.find(dom)
    end = start+len(dom)
    if(singleTag):
      ele = convert2Dic(dom)
      ele['innerText']=""
      ele['text']=""
      return (ele,start,end)
    tagLen = len(tag)+3
    while True:
      count = _getTagCount(dom,tag)
      if(count>0):
        count2 = _getTagCount(dom,"/"+tag+">")-1
        if(count==count2): break
        count -= count2
        while(count>0):
          count-=1
          tmp = html.find('</'+tag+'>', end)+tagLen
          if(tmp>tagLen):
            end=tmp

        dom = html[start:end]
      else:
        break
  
    html = re.compile('[\n\t]+').sub('', dom)#html[start:end])
    e2 = html.find('>')+1
    ele = convert2Dic(html[0:e2]+'</'+tag+'>')
    ele['innerHtml']=(html[e2:len(html)-tagLen]).strip()
    if(not ele['innerHtml']):
      ele['innerText']=""
      ele['text']=""
    else:
      innerText = re.compile('<[^>]+?>').sub('',ele['innerHtml'])
      ele['innerText']=re.sub('(\\s|&nbsp;)+', ' ', innerText.strip(), 0)
      ele['text']=ele['innerText']
    return (ele,start,end)
  return None

def getElementByID(id,html,start=None,end=None,before=None):
  return getElementByAttr('id',id,html,start,end,before)
  
def _getTag(html, end, attr):
  start = html.rfind('<',0,end)
  if(start >= 0 and end-start<300):
    if(attr and html[start:end].find(attr)<0):
      return None
    pattern = re.compile(u'<[\s]*?(?P<tag>[\S]*?)[\s]')
    html = html[start:end]
    tmp = pattern.search(html)
    if tmp: 
      tag = tmp.group("tag")
      if(re.compile(u'^[0-9a-zA-Z_.]+$').match(tag)):
        return tag
  return None

def getElementsByClass(className,html,start=None,end=None,before=None):
  lst=[]
  s=start
  h=html
  while True:
    obj = _getElement(None,'class',className,h,s,end,before)
    if(obj and obj[0]):
      lst.append(obj[0])
      h=h[obj[2]:]
      s=None
      end=None
    else:
      break
  return lst

def getElements(tag,attr='class',value=None,html=None,start=None,end=None,before=None):
  lst=[]
  s=start
  h=html
  while True:
    obj = _getElement(tag,attr,value,h,s,end,before)
    if(obj and obj[0]):
      lst.append(obj[0])
      h=h[obj[2]:]
      s=None
      end=None
    else:
      break
  return lst

def getElement(tag,attr='class',value=None,html=None,start=None,end=None,before=None):
  obj = _getElement(tag,attr,value,html,start,end,before)
  if(obj):
    return obj[0]
  return None
def _getElement(tag,attr='class',value=None,html=None,start=None,end=None,before=None):
  if(not value or not attr):
    return _getElementByTag(tag,html,start,end,before)

  if(not attr or not value or not html or html.find(value)<0): return None
  section = getSection(html,start,end,before)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return None

  html = html[s:e]
  if(not html): return None
  index = 0
  if(not tag):
    while index>=0:
      index = html.find(value,index)
      if(index<0): return None
      tag = _getTag(html,index,attr)
      if not tag: 
        index+=1
        continue
      else: break
  if not tag: return None
  singleTag = _checkSingleTag(tag)
  if(singleTag):
    strP = u'<[\s]*'+tag+'[^>]+?'+attr+'[=\'"\s]+(|[ \w]+[ ])'+value+'[ \'"][\s\S]*?>'
  else:
    strP = u'<[\s]*'+tag+'[^>]+?'+attr+'[=\'"\s]+(|[ \w]+[ ])'+value+'[ \'"][\s\S]*?>[\s\S]*?</'+tag+'>'
  pattern = re.compile(strP) 
  m = pattern.search(html)
  if m: 
    dom = m.group(0)
    start = html.find(dom)
    end = start+len(dom)
    if(singleTag):
      ele = convert2Dic(dom)
      ele['innerText']=""
      ele['text']=""
      return (ele,start,end)
    tagLen = len(tag)+3
    while True:
      count = _getTagCount(dom,tag)
      if(count>0):
        count2 = _getTagCount(dom,"/"+tag+">")-1
        if(count==count2): break
        count -= count2
        while(count>0):
          count-=1
          tmp = html.find('</'+tag+'>', end)+tagLen
          if(tmp>tagLen):
            end=tmp

        dom = html[start:end]
      else:
        break
    
    html = re.compile('[\n\t]+').sub('', dom)
    e2 = html.find('>')+1
    ele = convert2Dic(html[0:e2]+'</'+tag+'>')
    ele['innerHtml']=(html[e2:len(html)-tagLen]).strip()
    if(not ele['innerHtml']):
      ele['innerText']=""
      ele['text']=""
    else:
      innerText = re.compile('<[^>]+?>').sub('',ele['innerHtml'])
      ele['innerText']=re.sub('(\\s|&nbsp;)+', ' ', innerText.strip(), 0)
      ele['text']=ele['innerText']
    return (ele,start,end)
  return None
def _getTagCount(html,tag):
  tag='<'+tag
  tagLen=len(tag)
  count=0
  i=1
  while(i>0):
    s=html.find(tag,i+tagLen)
    if(s>0):
      count+=1
    i=s
  return count
def getElementBy(attr,value,html,start=None,end=None,before=None):
  return getElementByAttr(attr,value,html,start,end,before)

def getElementByAttr(attr,value,html,start=None,end=None,before=None):
  return getElement(None,attr=attr,value=value,html=html,start=start,end=end,before=before)

def getElementByClass(className,html,start=None,end=None,before=None):
  return getElementByAttr('class',className,html,start,end,before)

def getElementTextByID(id,html,start=None,end=None,before=None):
  return getElementByAttr('id',id,html,start,end,before)

def getParent(tag=None,attr=None,value=None,html=None,start=None,end=None,before=None):
  ele = _getElement(tag,attr,value,html,start,end,before)
  if(ele):
    start = ele[1]
    start = _getStart(html,start)
    end = ele[2]
    end = _getEnd(html,end)
    if(start and end):
      html = html[start:end]
      e2 = html.find('>')+1
      ele = convert2Dic(html[0:e2])
      ele['innerHtml']=(html[e2:len(html)]).strip()
      innerText = re.compile('<[^>]+?>').sub('',ele['innerHtml'])
      ele['innerText']=re.sub('(\\s|&nbsp;)+', ' ', innerText.strip(), 0)
      ele['text']=ele['innerText']
      return ele
  return None
def _getEnd(html,start):
  s = start
  startCount=0
  while(True):
    s = html.find('<', s)
    if(s<0): return None
    if(html[s+1:s+2]!='/'): 
      if(not _checkSingle(html,s)):
        startCount+=1
    else:
      if(startCount==0):
        return s
      startCount -= 1
    s+=1

def _getStart(html,end):
  s=0
  e=end
  endCount=0
  while(True):
    s = html.rfind('<',0,e)
    if(s<0): return None
    if(html[s+1:s+2]=='/'): 
      endCount+=1
    else:
      if (not _checkSingle(html,s)):
        if(endCount==0):
          return s
        endCount -= 1
    e=s-1
  
def _checkSingle(html,start=None):
  end = html.find('>',start)
  return html[end-1:end]=='/'
def getChildren(html,tag=None,start=None,end=None,before=None):
  if(tag):
    return getElementsByTag(tag,html,start,end,before)
  else:
    lst=[]
    section = getSection(html,start,end,before)
    if(section[1]<=section[0]):
      return lst
    h=html[section[0]:section[1]]
    s=0
    while True:
      tag = _getNextTag(h,s)
      obj = _getElementByTag(tag,h,s)
      if(obj and obj[0] and obj[2]>0):
        lst.append(obj[0])
        s+=obj[2]
      else:
        break
    return lst
def _getNextTag(html,start):
  pattern = re.compile(u'<[\s]*(?P<tag>[a-zA-Z0-9]+?)[/>\s]')
  tmp = pattern.search(html[start:])
  if tmp: 
    return tmp.group("tag")
  return None
def getNexts(attr,value,html,tag=None,start=None,end=None,before=None):
  ele = _getElement(tag,attr,value,html,start,end,before)
  if(ele):
    start = ele[2]
    end = _getEnd(html,start)
    if(start and end):
      html = html[start:end]
      return getChildren(html)
  return None
