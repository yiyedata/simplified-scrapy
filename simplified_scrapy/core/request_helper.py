#!/usr/bin/python
#coding=utf-8

import urllib
import json,copy
import sys,socket,random,time,re
import traceback,logging
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from simplified_scrapy.core.utils import printInfo,getTime,saveFile
if sys.version_info.major == 2:
  import urllib2
else:
  import urllib.request as urllib2
try:
  import spider_resource
except ImportError:
  spider_resource = None

class RequestError(Exception):
    def __init__(self,ErrorInfo,url=None):
        Exception.__init__(self,ErrorInfo)
        self.errorinfo=ErrorInfo
        self.url=url
    def __str__(self):
      if(self.url):
        return str(self.errorinfo)+"\n"+self.url
      else:
        return self.errorinfo

def log(err,data):
  printInfo(err,data)
  logger = logging.getLogger()
  logging.LoggerAdapter(logger, None).log(logging.ERROR, err)
  logging.LoggerAdapter(logger, None).log(logging.ERROR, data)
_userAgent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
_accept='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
_acceptJson='application/json, text/plain, */*'
_contentType='application/x-www-form-urlencoded'
_contentTypeJson='application/json'
_defaultHeader={
  'User-Agent':_userAgent,
  'Accept':_accept,
  }
_jsonHeader={
  'User-Agent':_userAgent,
  'Accept':_acceptJson
}
_defaultHeaderPost={
  'User-Agent':_userAgent,
  'Accept':_accept,
  'Content-Type':_contentType
  }
_jsonHeaderPost={
  'User-Agent':_userAgent,
  'Accept':_acceptJson,
  'Content-Type': _contentTypeJson
}
def _getMaintype(res):
  if sys.version_info.major == 2:
    maintype = res.headers.maintype
  else: 
    maintype =res.info().get('Content-Type')
  return maintype
def _checkMaintype(maintype):
  types = ['xml','plain','text','html','json']
  for t in types:
    if(maintype.find(t)>=0):
      return True
  return False
def requestPost(url, data, headers=None, useIp=False, ssp=None,timeout=30,error=False):
  response = None
  _head = _defaultHeaderPost
  if(data and isinstance(data,dict)):
    _head = _jsonHeaderPost
    data = json.dumps(data)
  if headers: header = headers
  else: header = copy.deepcopy(_head)
  useragent = None
  proxyips = None
  if ssp:
    useragent = ssp.useragent
    proxyips = ssp.proxyips
  if(not useragent):
    if(spider_resource and spider_resource.useragent):
      useragent = spider_resource.useragent
  if(not proxyips):
    if(spider_resource and spider_resource.proxyips):
      proxyips = spider_resource.proxyips
  try:
    if(headers and not headers.get('User-Agent') and useragent):
      header['User-Agent']=random.choice(useragent)
    # if(not header.get('User-Agent')):
    #   header['User-Agent']=_head['User-Agent']
    # if(not header.get('Accept')):
    #   header['Accept']=_head['Accept']
    if(sys.version_info.major==3):
      if(data): data=data.encode("utf-8")
    req = urllib2.Request(url, data, header)
    
    if(ssp):
      req = ssp.beforeRequest(url, req)
    opener = None
    if(useIp or (ssp and (ssp.use_ip or ssp.proxyips))):
      p = url[0:url.index(':')]
      if(proxyips and proxyips.get(p)):
        opener = _setProxy(p, random.choice(proxyips[p]))
    if(not opener): opener = urllib2.build_opener()
    
    response = opener.open(req,None,timeout)
    if(ssp):
      if error:
        return ssp.afterResponse(response,url,error)
      else:
        return ssp.afterResponse(response,url)
    return getResponseStr(response,url,error)
  except Exception as err:
    if(not error):
      log(err,url)
    else:
      raise RequestError(err,url)
  finally:
    if response and _checkMaintype(_getMaintype(response)): 
      response.close()
  return "_error_"

def getResponseStr(res,url,error=False):
  html="_error_"
  if(not _checkMaintype(_getMaintype(res))):
    return res
  htmSource = res.read()
  try:
    html=htmSource.decode("utf-8")
  except:
    try:
      html=htmSource.decode("gb18030")
    except Exception as err:
      if(not error):
        log(err.reason or err.message,url)
      else:
        return res
      # try:
      #   html=str(htmSource).decode("string_escape")
      # except Exception as err:
      #   log(err.reason,url)
  return html
def setProxyGloab(proxy):
  proxy_handler = urllib2.ProxyHandler({proxy['p']:proxy['ip']})
  opener = urllib2.build_opener(proxy_handler)  
  urllib2.install_opener(opener)  
def _setProxy(p,ip):
  if(not p or not ip): return None
  proxy_handler = urllib2.ProxyHandler({p:ip})
  opener = urllib2.build_opener(proxy_handler)  
  return opener
def dic2tuple(dic):
  tp=[]
  for key in dic:
    tp.append((key,dic[key]))
  return tp

def requestGet(url, headers, useIp, ssp=None,timeout=30,error=False):
  response = None
  _head = _defaultHeader
  if(url[-5:].lower()=='.json'):
    _head = _jsonHeader
  if headers: header = headers 
  else: header = copy.deepcopy(_head)
  useragent = None
  proxyips = None
  if ssp:
    useragent = ssp.useragent
    proxyips = ssp.proxyips
  if(not useragent):
    if(spider_resource and spider_resource.useragent):
      useragent = spider_resource.useragent
  if(not proxyips):
    if(spider_resource and spider_resource.proxyips):
      proxyips = spider_resource.proxyips
  try:
    if(headers and not headers.get('User-Agent') and useragent):
      header['User-Agent'] = random.choice(useragent)
    # if(not header.get('User-Agent')):
    #   header['User-Agent']=_defaultHeader['User-Agent']
    # if(not header.get('Accept')):
    #   if(url[-5:].lower()=='.json'):
    #     header['Accept']=_jsonHeader['Accept']
    #   else:
    #     header['Accept']=_defaultHeader['Accept']
      
    req = urllib2.Request(url, None, header)
    if(ssp): 
      req = ssp.beforeRequest(url, req)

    opener = None
    if(useIp or (ssp and (ssp.use_ip or ssp.proxyips))):
      p = url[0:url.index(':')]
      if(proxyips and proxyips.get(p)):
        opener = _setProxy(p, random.choice(proxyips[p]))
    if(not opener): opener = urllib2.build_opener()

    response = opener.open(req,None,timeout)
    if(ssp): 
      if(error):
        data = ssp.afterResponse(response,url,error)
      else:
        data = ssp.afterResponse(response,url)
    else: 
      data = getResponseStr(response,url,error)
    return data
  except Exception as err:
    if(not error):
      log(err,url)
    else:
      raise RequestError(err,url)
  finally:
    if response and _checkMaintype(_getMaintype(response)): 
      response.close()
  return "_error_"
def extractHtml(url,html,model,modelName,title=None):
  # headers = { "Content-Type": "application/json" }
  data={
    'url':url,
    'title':title,
    'html':html,
    'model':json.dumps(model),
    'key':"yiyedata_test" 
  }
  if(modelName): 
    data['modelName']=json.dumps(modelName)
  
  # data = json.dumps(data)
  obj = requestPost('http://www.yiyedata.com/api/extracts',data)
  return obj#.decode("UTF-8").encode(type)

def test():
  printInfo('start')
  user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'# 将user_agent写入头信息 
  headers = { 'User-Agent' : user_agent, "Content-Type": "application/json",#"Content-Length":len(data), 
    "Referer":"http://47.92.87.212:8080/yiye.mgt/view/login.jsp"
  } 
  obj={
    'url':'http://health.sina.com.cn/',
    'title':'北京冬奥会世界新闻机构会议在京举办',
    'html':"",  
    'modelName':'["auto_obj","auto_url"]',
    'model':'[{"Type":3},{"Type":2,"UrlDomains": "all_domain"}]',
    'key':"yiyedata_test" 
  }
  data = json.dumps(obj)
  # data = urllib.urlencode(values)  
  printInfo(requestPost('http://www.yiyedata.com/api/extracts',data,headers,None))
# test()
# model=['{"Type":2}','{"Type":3}']
# print json.dumps(model)

# print (requestGet('https://blog.csdn.net',None,None,timeout=30))
