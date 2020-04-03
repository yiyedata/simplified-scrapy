#!/usr/bin/python
#coding=utf-8
import re,json
import sys
from simplified_scrapy.core.utils import printInfo,absoluteUrl,md5
from simplified_scrapy.core.xml_helper import XmlDictConfig,convert2Dic
from simplified_scrapy.core.dictex import Dict

__regCache={}
def _getRegex(regex):
  if not __regCache.get(regex):
    __regCache[regex] = re.compile(regex)
  return __regCache[regex]
def getSection(html,start=None,end=None,before=None):
  if not html: return (0,0)
  s = 0
  e = len(html)
  if(start): 
    if(isinstance(start,int)): s=start
    else:
      if isinstance(start,list):
        for st in start:
          s=html.find(st)
          if s>=0: break
      else:
        s=html.find(start)
  if(end): 
    if(isinstance(end,int)): e=end
    else: 
      if isinstance(end,list):
        for st in end:
          e=html.find(st,s)
          if e>=0: break
      else:
        e=html.find(end,s)
  if(before):
    if(isinstance(before,int)): s=before
    else: 
      if isinstance(before,list):
        for st in before:
          s=html.find(st,0,e)
          if s>=0: break
      else:
        s=html.rfind(before,0,e)
  return (s,e)
def listA(html,baseUrl=None,start=None,end=None,before=None):
  if(not html): return []
  section = getSection(html,start,end,before)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return []
  html = html[s:e]
  if(not html or html.find("<a")<0): return []

  patternLst = _getRegex(u'<a[\s]+[^>]*>[\s\S]*?</a>')
  patternUrl = _getRegex(u'href[\s]*=[\s\'"]*(?P<url>.*?)[\'"\s>]') 
  patternTitle1 = _getRegex(u'title[\s]*=[\s\'"]*(?P<title>.*?)[\'"\s>]')
  patternTitle2 = _getRegex(u'<a[\s]+[^>]*>(?P<title>.*?)</a>')

  strA = patternLst.findall(html)
  dic = Dict()
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
        title = _getRegex('<[^<>]+>').sub('',title)

    try:
      if(url):
        url = url.strip().lower()
        if(baseUrl and url[:7]!="http://" and  url[:8]!="https://"):
          absUrl = absoluteUrl(baseUrl,url)
          if(absUrl!=url):
            d = dic[absUrl]
            if d:
              if not d.title or (title and len(d.title)<len(title)):
                d['title'] = title
            else:
              dic[absUrl] = Dict({'url':absUrl,'title':title,'relativeUrl':url})
        else:
          if url.rfind('/')<9:
            url += '/'
          d = dic[url]
          if d:
            if not d.title or (title and len(d.title)<len(title)):
              d['title'] = title
          else:
            dic[url] = Dict({'url':url,'title':title})
    except Exception as ex:
      printInfo(ex)
    
  return list(dic.values())

def getListByReg(html,regex,group=0,start=None,end=None,before=None):
  if(not html or not regex): return []
  section = getSection(html,start,end,before)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return []
  html = html[s:e]
  if not group:
    patternLst = _getRegex(regex)
    strs = patternLst.findall(html)
  else:
    strs = []
    while s>=0:
      block = getOneByReg(html,regex,group)
      if block:
        strs.append(block)
        s=html.find(block)+len(block)
        html=html[s:]
      else:
        break
  return strs

def getOneByReg(html,regex,group=0,start=None,end=None,before=None):
  if(not html or not regex): return None
  section = getSection(html,start,end,before)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return None
  html = html[s:e]
  patternLst = _getRegex(regex)
  tmp = patternLst.search(html)
  if tmp:
    return tmp.group(group)
  return None

def listImg(html,baseUrl=None,start=None,end=None,before=None):
  if(not html or html.find("<img")<0): return []
  section = getSection(html,start,end,before)
  s = section[0]
  e = section[1]

  if(s < 0 or e < s): return None
  html = html[s:e]
  if(not html or html.find("<img")<0): return None

  patternLst = _getRegex(u'<img[\s]+[^>]*>')
  patternUrl = _getRegex(u'src[\s]*=[\s\'"]*(?P<url>.*?)[\'"\s>]') 
  patternTitle = _getRegex(u'alt[\s]*=[\s\'"]*(?P<title>.*?)[\'"\s>]')
  lstStr = patternLst.findall(html)
  # lst=[]
  dic = Dict()
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
        url = url.strip().lower()
        if(baseUrl and url[:7]!="http://" and  url[:8]!="https://"):
          absUrl = absoluteUrl(baseUrl,url)
          if(absUrl!=url):
            d = dic[absUrl]
            if d:
              if not d.alt or (title and len(d.alt)<len(title)):
                d['alt'] = title
            else:
              dic[absUrl] = Dict({'url':absUrl,'alt':title, 'relativeUrl':url})
            # lst.append(Dict({'url':absUrl,'alt':title, 'relativeUrl':url}))
        else:
          d = dic[url]
          if d:
            if not d.alt or (title and len(d.alt)<len(title)):
              d['alt'] = title
          else:
            dic[url] = Dict({'url':url,'alt':title})
          # lst.append(Dict({'url':url,'alt':title}))
    except Exception as ex:
      printInfo(ex)
    
  return list(dic.values())
__re0=re.compile('<[^<>]+>')
def preDealHtml(html):
  html = __re0.sub(_replaceHtml,html) # script?
  return html
__re1=re.compile('[\s]*>')
__re2=re.compile('<[\s]*')
__re3=re.compile('[\s]*/>')
__re4=re.compile('[\s]+')
def _replaceHtml(value):
  html = value.group()
  html = __re1.sub('>',html)
  html = __re2.sub('<',html) # script?
  html = __re3.sub(' />',html) # script?
  return __re4.sub(' ',html)

def removeScripts(html):
  if (not html): return html
  html = _getRegex('<!--[\s\S]*?-->').sub('',html)
  html = _getRegex('<[\s]*script[^>]*>[\s\S]*?</script>').sub('',html)
  html = _getRegex('<[\s]*style[^>]*>[\s\S]*?</style>').sub('',html)
  html = _getRegex('<[\s]*link [\s\S]*?>').sub('',html)
  html = _getRegex('<[\s]*meta [\s\S]*?>').sub('',html)
  html = _getRegex('<[\s]*object[^>]*>[\s\S]*?</object>').sub('',html)
  html = _getRegex('<[\s]*iframe[^>]*>[\s\S]*?</iframe>').sub('',html)
  html = _getRegex('</object>').sub('',html)
  html = _getRegex('<param [\s\S]*?>').sub('',html)
  return html
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
def _checkSingleTag(tag,html=None,i=0):
  tags = ['br','hr','img','input','param','meta','link']
  if tag.lower() in tags: return True
  if not html: return False
  index1 = html.find('<'+tag+' ',i)
  if index1<0: 
    index1 = html.find('<'+tag+'/>',i)
    if index1>=0: return True
  index2 = html.find('<'+tag+'>',i)
  if index2>-1 and index2<index1: return False
  if index1<0:
    index1 = index2
  end = html.find('>',index1)
  if html[end-1]=='/': return True
  return False
def _getElementByTag(tag,html,start=None,end=None,before=None):
  if(not tag or not html): return None
  section = getSection(html,start,end,before)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return None

  html = html[s:e]
  if(not html): return None
  if isinstance(tag,list):
    tags = tag
    index = len(html)
    for t in tags:
      tmp1 = html.find('<'+t +' ')
      tmp2 = html.find('<'+t +'>')
      if tmp1>=0 and tmp2>=0:
        if index>min(tmp1,tmp2):
          tag = t
          index = min(tmp1,tmp2)
      elif tmp1>=0 and tmp1<index:
        tag = t
        index = tmp1
      elif tmp2>=0 and tmp2<index:
        tag = t
        index = tmp2
  if isinstance(tag,list) or html.find('<'+tag)<0: return None
  singleTag = _checkSingleTag(tag, html)
  if(singleTag):
    pattern = _getRegex(u'<'+_dealRegChar(tag)+'([\s]+|)[^>]*?>') 
  else:
    pattern = _getRegex(u'<'+_dealRegChar(tag)+'([\s]+[^>]*?>|>)[\s\S]*?</'+_dealRegChar(tag)+'>') 
  m = pattern.search(html)
  if m: 
    dom = m.group(0)
    start = html.find(dom)
    end = start+len(dom)
    if(singleTag):
      ele = convert2Dic(dom)
      ele._start=start+s
      ele._end=end+s
      return (ele,start,end)
    tagLen = len(tag)+3
    while True:
      count = _getTagCount(dom,['<'+tag+' ','<'+tag+'>'])
      if(count>0):
        count2 = _getTagCount(dom,["</"+tag+">"])-1
        if(count==count2 or count2<0): break
        count -= count2
        while(count>0):
          count-=1
          tmp = html.find('</'+tag+'>', end)+tagLen
          if(tmp>tagLen):
            end=tmp
          else:
            return None
        dom = html[start:end]
      else:
        break
  
    html = dom
    e2 = html.find('>')+1
    ele = convert2Dic(html[:e2]+'</'+tag+'>')
    ele['html']=(html[e2:len(html)-tagLen])#.strip()
    ele._start=start+s
    ele._end=end+s
    return (ele,start,end)
  return None
__reh0=re.compile('<!--[\s\S]*?-->')
__reh1=re.compile('<[^<>]+>')
__reh2=re.compile('(\s|&nbsp;)+')
__reh3=re.compile('(\s*_yazz_\s*)+')
def removeHtml(html,replace='',tags=None):
  if not html: return html
  innerText = __reh0.sub('',html)
  if not tags:
    tags = ['br','p']
  while innerText.find('>')>=0:
    text = innerText
    if replace:
      for tag in tags:
        text = _getRegex('<[/]*'+tag+'[^<>]+>').sub('_yazz_',text)
    text = __reh1.sub('',text)
    if text == innerText:
      break
    innerText = text
  innerText = __reh2.sub(' ', innerText.strip())
  if replace:
    innerText = __reh3.sub(replace, innerText)
  return innerText.strip().strip(replace)

def replaceReg(html, regex, new, count = 0):
  return re.sub(_getRegex(regex), new, html, count)

def trimHtml(html):
  if(not html): return html
  html = html.strip()
  start = html.find('>')
  tmp = html.find('<')
  if(start<0 and tmp<0): return html
  if(tmp<0): return html[start+1:]
  if(start<0): return html[:tmp]
  if(start>tmp): 
    start = 0
  else:
    start = start+1
  end = html.rfind('<')
  tmp = html.rfind('>')
  if(end>tmp): return html[start:end]
  else: return html[start:]

def getElementByID(id,html,start=None,end=None,before=None):
  return getElementByAttr('id',id,html,start,end,before)
  
def checkContains(html, reg):
  return not not _getRegex(reg).search(html)

def _getTag(html, end, attr, start=None):
  if start==None: start = html.rfind('<',0,end)
  checkStart = html.rfind('>',0,end)
  if start < checkStart: end = checkStart+1
  if(start >= 0 and end-start<300):
    if(attr and html[start:end].find(attr)<0):
      return None
    pattern = _getRegex(u'<?(?P<tag>[\S]*?)[\s/>]')
    html = html[start:end]
    tmp = pattern.search(html)
    if tmp: 
      tag = tmp.group("tag")
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
      # h=h[obj[2]:]
      s=obj[0]._end
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
      # h=h[obj[2]:]
      s=obj[0]._end
      before=None
    else:
      break
  return lst

def getElement(tag,attr='class',value=None,html=None,start=None,end=None,before=None):
  obj = _getElement(tag,attr,value,html,start,end,before)
  if(obj):
    return obj[0]
  return None
def removeElement(tag,attr='class',value=None,html=None,start=None,end=None,before=None):
  obj = _getElement(tag,attr,value,html,start,end,before)
  if(obj):
    return html[0:obj[0]._start]+html[obj[0]._end:]
  return html
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
  flagTag = False
  while True:
    if(not tag):
      flagTag = True
      while index>=0:
        index = html.find(value,index)
        if(index<0): return None
        tag = _getTag(html,index,attr)
        if not tag: 
          index+=1
          continue
        else: break
    if not tag: return None
    if isinstance(tag,list):
      tags = tag
      index = len(html)
      for t in tags:
        tmp1 = html.find('<'+t +' ')
        tmp2 = html.find('<'+t +'>')
        if tmp1>=0 and tmp2>=0:
          if index>min(tmp1,tmp2):
            tag = t
            index = min(tmp1,tmp2)
        elif tmp1>=0 and tmp1<index:
          tag = t
          index = tmp1
        elif tmp2>=0 and tmp2<index:
          tag = t
          index = tmp2
    if isinstance(tag,list) or html.find('<'+tag)<0: return None
    singleTag = _checkSingleTag(tag,html,index)
    value = _dealRegChar(value)
    if(singleTag):
      strP = u'<'+_dealRegChar(tag)+'[\s]+[^>]*?'+_dealRegChar(attr)+'[=\'"\s]+([\w\-\.]+[\s\w\-\.]*[ ]|\s*|)'+value+'([\s\'"][\s\S]*?|)>'
    else:
      strP = u'<'+_dealRegChar(tag)+'[\s]+[^>]*?'+_dealRegChar(attr)+'[=\'"\s]+([\w\-\.]+[\s\w\-\.]*[ ]|\s*|)'+value+'([\s\'"][\s\S]*?|)>[\s\S]*?</'+_dealRegChar(tag)+'>'
    pattern = _getRegex(strP) 
    m = pattern.search(html)
    if m: 
      dom = m.group(0)
      start = html.find(dom)
      end = start+len(dom)
      if(singleTag):
        ele = convert2Dic(dom)
        ele._start=start+s
        ele._end=end+s
        return (ele,start,end)
      tagLen = len(tag)+3
      while True:
        count = _getTagCount(dom,['<'+tag+' ','<'+tag+'>'])
        if(count>0):
          count2 = _getTagCount(dom,["</"+tag+">"])-1
          if(count==count2 or count2<0): break
          count -= count2
          while(count>0):
            count-=1
            tmp = html.find('</'+tag+'>', end)+tagLen
            if(tmp>=tagLen):
              end=tmp
            else:
              return None

          dom = html[start:end]
        else:
          break
      
      html = dom
      e2 = html.find('>')+1
      ele = convert2Dic(html[0:e2]+'</'+tag+'>')
      ele['html']=(html[e2:len(html)-tagLen])#.strip()
      ele._start=start+s
      ele._end=end+s
      return (ele,start,end)
    else:
      if not flagTag:
        return None
      else: 
        index += 1
        tag = None
        if index>=len(html): return None
  return None
def _dealRegChar(value):
  kvs = [('\\','\\\\'),('(','\('),(')','\)'),('$','\$'),('*','\*'),('+','\+'),('{','\{'),('}','\}'),
    ('?','\?'),('^','\^'),('|','\|'),('[','\['),(']','\]'),('.','\.')]
  for kv in kvs:
    value = value.replace(kv[0],kv[1])
  return value
def _getStartByReg(regex,html,start):
  pattern = _getRegex(regex) 
  m = pattern.search(html[start:])
  if m: 
    dom = m.group(0)
    return html.find(dom,start)
    # end = start+len(dom)
  return -1
def getElementByReg(regex, tag=None, html=None,start=None,end=None,before=None):
  if(not regex or not html): return None
  section = getSection(html,start,end,before)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s or s==e): return None
  html = html[s:e]
  start = _getStartByReg(regex,html,0) # html.find(text,start)
  if start<0: return None
  start = html.rfind('<',0,start)

  if not tag: tag=''
  selectStr = '<'+tag
  start = html.rfind(selectStr,0,start+len(selectStr))
  end = html.find('>',start)+1
  tagLeft=html[start:end]
  if not tag:
    tag = _getTag(tagLeft,len(tagLeft),None,0)
  return getElementByTag(tag,html,start)

def getElementByText(text, tag=None, html=None,start=None,end=None,before=None):
  if(not text or not html): return None
  section = getSection(html,start,end,before)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return None
  html = html[s:e]
  start = 0
  while True:
    start = html.find(text,start)
    if start<0: return None
    l = html.rfind('<',0,start)
    r = html.find('<',start)
    rr = html.find('>',start,r)
    if html.find('>',l,start)>0 and rr<0:
      break
    start = rr

  if not tag: tag=''
  selectStr = '<'+tag
  start = html.rfind(selectStr,0,start)
  end = html.find('>',start)+1

  tagLeft=html[start:end]
  if not tag:
    tag = _getTag(tagLeft,len(tagLeft),None,0)
  return getElementByTag(tag,html,start)
  
def _getTagCount(html,tags):
  count=0
  for t in tags:
    tagLen=len(t)
    i=0
    while(i>=0):
      s=html.find(t,i+tagLen)
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

def getParent(tag=None,attr=None,value=None,html=None,start=None,end=None,before=None):
  ele = _getElement(tag,attr,value,html,start,end,before)
  return getParent4Ele(html,ele)
def getParent4Ele(html,e,tag=None):
  if(e):
    start = e._start
    p = _getParentStart(html,start,tag)
    if not p: return None
    start,tag = p
    end = e._end
    end = _getParentEnd(html,end,tag)
    # if e.tag == tag:
    #   end = _getEnd4Tag(html,end+1,tag)
    if(start !=None and end!=None):
      h = html[start:end]
      e2 = h.find('>')+1
      ele = convert2Dic(h[0:e2])
      ele['html']=(h[e2:len(h)-len(tag)-3])
      ele._start=start
      ele._end=end #html.find('>',end)+1
      return ele
  return None
def _getParentEnd(html,start,tag):
  end = start
  while True:
    if end<0: return None
    l = html.find('<'+tag,end)
    r = html.find('</'+tag,end)
    if r>0 and (l>r or l<0): return r+len(tag)+3
    if r>l: end=r+len(tag)+3
    else: return None
def _getParentStart(html,end,tag):
  start = end
  s = end
  dicTag=Dict()
  if not tag:
    while True:
      if s<0: return None
      l = html.rfind('<',0,s)
      r = html.rfind('>',0,s)
      if (r<l or l<0 or r<0): return None
      tagHtml = html[l:r+1]
      if tagHtml[1]=='/': 
        s = l
        tmpTag = tagHtml[2:-1]
        if not dicTag[tmpTag]:
          dicTag[tmpTag]=1
        else:
          dicTag[tmpTag]=dicTag[tmpTag]+1
        continue
      tag = _getTag(tagHtml,r-l+1,None,0)
      if len(dicTag)>0:
        if dicTag[tag]:
          dicTag[tag]=dicTag[tag]-1
          if not dicTag[tag]:
            del dicTag[tag]
        s = l
        continue
      if not tag: return None
      if _checkSingle(tagHtml,0):
        start = html.rfind('<'+tag,0,start)
        continue
      l = html.rfind('<'+tag,0,start)
      r = html.rfind('</'+tag,0,start)
      if l>r: return (l,tag)
      if r>l: 
        start=l
        s=l
      else: return None
  else:
    while True:
      if start<0: return None
      l = html.rfind('<'+tag,0,start)
      r = html.rfind('</'+tag,0,start)
      if l>r: return (l,tag)
      if r>l: start=l
      else: return None

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
def _getEnd4Tag(html,start,tag):
  if not tag:
    return _getEnd(html,start)
  s = start
  while(True):
    s = html.find('</'+tag, s)
    ss = html.find('<'+tag, s)
    if(s<0): return None
    if ss<0 or ss>s:
      return s + len(tag)+3
    s+=1
def _getStart4Tag(html,end,tag):
  if not tag: 
    return _getStart(html,end)
  s=0
  e=end
  while(True):
    s = html.rfind('<'+tag,0,e)
    se = html.rfind('</'+tag,0,e)
    if(s<0): return None
    if se<0 or se<s:
      return s
    e=s-1
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
  flag = html[end-1:end]=='/'
  if flag: return True
  tag = _getTag(html,end+1,None,start)
  if not tag: return False
  return _checkSingleTag(tag)
def getChildren(html,tag=None,start=None,end=None,before=None):
  lst=[]
  if(tag):
    lst = getElementsByTag(tag,html,start,end,before)
  else:
    section = getSection(html,start,end,before)
    if(section[1]<=section[0]):
      return lst
    h=html[:section[1]]
    s=section[0]
    while True:
      tag = _getNextTag(h,s)
      obj = _getElementByTag(tag,h,s)
      if(obj and obj[0] and obj[2]>0):
        lst.append(obj[0])
        s=obj[0]._end
      else:
        break
  return lst
def getChild(html,tag=None,start=None,end=None,before=None):
  if(tag):
    return getElementByTag(tag,html,start,end,before)
  else:
    section = getSection(html,start,end,before)
    if(section[1]<=section[0]):
      return None
    h=html[:section[1]]
    s=section[0]
    tag = _getNextTag(h,s)
    obj = _getElementByTag(tag,h,s)
    if(obj and obj[0] and obj[2]>0):
      return obj[0]
  return None
def _getNextTag(html,start):
  pattern = _getRegex(u'<[\s]*(?P<tag>[a-zA-Z0-9:_.-]+?)[/>\s]')
  tmp = pattern.search(html[start:])
  if tmp: 
    return tmp.group("tag")
  return None
def getNexts(attr,value,html,tag=None,start=None,end=None,before=None):
  ele = _getElement(tag,attr,value,html,start,end,before)
  return getNexts4Ele(html,ele)
def getNexts4Ele(html,ele,tag=None):
  if(ele):
    parent = getParent4Ele(html,ele,None)
    if parent:
      start = ele._end
      end = parent._end-len(parent.tag)-3
      html = html[start:end]
      lst = getChildren(html)
      for e in lst:
        e._end+=start
        e._start+=start
      return lst
    else:
      start = ele._end
      html = html[start:]
      lst = getChildren(html)
      for e in lst:
        e._end+=start
        e._start+=start
      return lst

  return []
def getNext4Ele(html,ele,tag=None):
  if(ele):
    start = ele._end
    return getChild(html,tag,start=start)
    # end = start
    # l = html.find('<',end)
    # r = html.find('>',end)
    # if (r<l or l<0 or r<0): return None
    # tagHtml = html[l:r+1]
    # tag = _getTag(tagHtml,r-l+1,None,0)
    # if not tag: return None
    # if _checkSingle(tagHtml,0):
    #   # start = html.find('<'+tag,start)
    #   end = html.find('>',end)+1
    # else:
    #   while True:
    #     l = html.find('<'+tag,end)
    #     r = html.find('</'+tag,end)
    #     if r>=0 and (l>r or l<0) : 
    #       end = r+len(tag)+3
    #       break
    #     if r>l: end=r+len(tag)+3
    #     else: return None



    # end = _getEnd4Tag(html,start,tag)
    # if not end:
    #   if html[start:start+2] != '</': end = len(html)
    # if(start != None and end != None):
    #   html = html[start:end]
    #   return getChild(html)
  return None
def getPrevious4Ele(html,ele,tag=None):
  if(ele):
    parent = getParent4Ele(html,ele,None)
    if parent:
      start = html.find('>',parent._start)+1
      end = ele._start
      html = html[start:end]
      lst = getChildren(html)
      for e in lst:
        e._end+=start
        e._start+=start
      return lst
    else:
      start = 0
      end = ele._start
      html = html[start:end]
      lst = getChildren(html)
      return lst
  return []

if __name__=='__main__':
  html = '''<asd asss> 
   qwe</asd>'''
  print (_getTag(preDealHtml(html),html.find('>'),None))