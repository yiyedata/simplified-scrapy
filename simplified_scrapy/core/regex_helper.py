#!/usr/bin/python
#coding=utf-8
import re,json
import sys
if sys.version_info.major == 2:
  from xml_helper import XmlDictConfig,convert2Dic
  from utils import absoluteUrl,printInfo
else:
  from .xml_helper import XmlDictConfig,convert2Dic
  from .utils import absoluteUrl,printInfo
def getSection(html,start=None,end=None):
  s = 0
  e = len(html)
  if(start): 
    if(isinstance(start,int)): s=start
    else: s=html.find(start)
  if(end): 
    if(isinstance(end,int)): e=end
    else: e=html.find(end)
  return (s,e)
def listA(html,baseUrl=None,start=None,end=None):
  if(not html): return []
  section = getSection(html,start,end)
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
def listImg(html,baseUrl=None,start=None,end=None):
  if(not html or html.find("<img")<0): return []
  section = getSection(html,start,end)
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

def getElementsByTag(tag,html,start=None,end=None):
  lst=[]
  section = getSection(html,start,end)
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

def getElementByTag(tag,html,start=None,end=None):
  obj = _getElementByTag(tag,html,start,end)
  if(obj and obj[0]):
    return obj[0]
  return None

def _getElementByTag(tag,html,start=None,end=None):
  if(not tag or not html or html.find(tag)<0): return None
  section = getSection(html,start,end)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return None

  html = html[s:e]
  if(not html): return None

  pattern = re.compile(u'<[\s]*'+tag+'[^>]*?>[\s\S]*?</'+tag+'>') 
  m = pattern.search(html)
  if m: 
    dom = m.group(0)
    start = html.find(dom)
    end = start+len(dom)
    tagLen = len(tag)+3
    i = html.find('>',start)
    while i>=0:
      i = html.find(tag, i, end-tagLen)
      if(i>=0):
        e = html.find('</'+tag+'>', end)
        if e<0: break
        i = end
        end = e+tagLen
        continue
    html = re.compile('[\n\t]+').sub('', html[start:end])
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

def getElementByID(id,html,start=None,end=None):
  return getElementByAttr('id',id,html,start,end)
  
def _getTag(html, end):
  start = html.rfind('<',0,end)
  if(start >= 0):
    pattern = re.compile(u'<[\s]*?(?P<tag>[\S]*?)[\s]')
    html = html[start:end]
    tmp = pattern.search(html)
    if tmp: 
      return tmp.group("tag")
  return None

def getElementsByClass(className,html,start=None,end=None):
  lst=[]
  s=start
  h=html
  while True:
    obj = _getElement(None,'class',className,h,s,end)
    if(obj and obj[0]):
      lst.append(obj[0])
      h=h[obj[2]:]
      s=None
      end=None
    else:
      break
  return lst

def getElements(tag,attr='class',value=None,html=None,start=None,end=None):
  lst=[]
  s=start
  h=html
  while True:
    obj = _getElement(tag,attr,value,h,s,end)
    if(obj and obj[0]):
      lst.append(obj[0])
      h=h[obj[2]:]
      s=None
      end=None
    else:
      break
  return lst

def getElement(tag,attr='class',value=None,html=None,start=None,end=None):
  obj = _getElement(tag,attr,value,html,start,end)
  if(obj):
    return obj[0]
  return None
def _getElement(tag,attr='class',value=None,html=None,start=None,end=None):
  if(not value or not attr):
    return _getElementByTag(tag,html,start,end)

  if(not attr or not value or not html or html.find(value)<0): return None
  section = getSection(html,start,end)
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
      tag = _getTag(html,index)
      if not tag: 
        index+=1
        continue
      else: break
  if not tag: return None

  pattern = re.compile(u'<[\s]*'+tag+'[^>]+?'+attr+'[=\'"\s]+'+value+'[\'"][\s\S]*?>[\s\S]*?</'+tag+'>') 
  m = pattern.search(html)
  if m: 
    dom = m.group(0)
    start = html.find(dom)
    end = start+len(dom)
    tagLen = len(tag)+3
    i = html.find('>',start)
    while i>=0:
      i = html.find(tag, i, end-tagLen)
      if(i>=0):
        e = html.find('</'+tag+'>', end)
        if e<0: break
        i = end
        end = e+tagLen
        continue
    html = re.compile('[\n\t]+').sub('', html[start:end])
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

def getElementBy(attr,value,html,start=None,end=None):
  return getElementByAttr(attr,value,html,start,end)

def getElementByAttr(attr,value,html,start=None,end=None):
  return getElement(None,attr=attr,value=value,html=html,start=start,end=end)

def getElementByClass(className,html,start=None,end=None):
  return getElementByAttr('class',className,html,start,end)

def getElementTextByID(id,html,start=None,end=None):
  return getElementByAttr('id',id,html,start,end)

def getElementAttrByID(id,attr,html,start=None,end=None):
  return getElementByAttr('id',id,html,start,end)
