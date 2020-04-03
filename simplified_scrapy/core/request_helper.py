#!/usr/bin/python
#coding=utf-8

import urllib
import json,copy
import sys,socket,random,time,re
import traceback,logging
from simplified_scrapy.core.zip_helper import decodeZip
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
try:
  from setting import extract_api_url,extract_api_key
except ImportError:
  extract_api_url = 'http://www.yiyedata.com/api/extracts'
  extract_api_key = 'yiyedata_python'

try:
  from setting import encodings as setting_encodings
except ImportError:
  setting_encodings={}

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
  'Accept-Encoding':'gzip, deflate'
  }
_jsonHeader={
  'User-Agent':_userAgent,
  'Accept':_acceptJson
}
_defaultHeaderPost={
  'User-Agent':_userAgent,
  'Accept':_accept,
  'Content-Type':_contentType,
  'Accept-Encoding':'gzip, deflate'
  }
_jsonHeaderPost={
  'User-Agent':_userAgent,
  'Accept':_acceptJson,
  'Content-Type': _contentTypeJson
}
_cache_encodings={}
def _getMaintype(res):
  if sys.version_info.major == 2:
    maintype = res.headers.type
  else: 
    maintype =res.info().get('Content-Type')
  return maintype
def _checkMaintype(maintype):
  types = ['xml','plain','text','html','json','javascript','java']
  for t in types:
    if(maintype.find(t)>=0):
      return True
  return False
def requestPost(url, data, headers=None, useIp=False, ssp=None,timeout=30,error=False, method=None):
  response = None
  _head = _defaultHeaderPost
  if(data and (isinstance(data,dict) or isinstance(data,list))):
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
    if(sys.version_info.major==3):
      if(data): data=data.encode("utf-8")
    req = urllib2.Request(url, data, header)
    if method: req.get_method = lambda:method.upper()
    if(ssp):
      req = ssp.beforeRequest(url, req)
    opener = None
    if(useIp or (ssp and (ssp.use_ip or ssp.proxyips))):
      p = url[0:url.index(':')]
      if(proxyips and proxyips.get(p)):
        opener = _setProxy(p, random.choice(proxyips[p]))
    if(not opener): opener = urllib2.build_opener()
    
    response = opener.open(req,None,timeout)
    if headers != None:
      cookie = _getCookie(response)
      if cookie:
        headers['newCookie']=cookie
    if(ssp):
      if error:
        return ssp.afterResponse(response,url,error)
      else:
        return ssp.afterResponse(response,url)
    return getResponseStr(response,url,ssp,error)
  except Exception as err:
    if(not error):
      log(err,url)
    else:
      raise RequestError(err,url)
  finally:
    if response and _checkMaintype(_getMaintype(response)): 
      response.close()
  return "_error_"
def _getCookie(response):
  if sys.version_info.major == 2:
    cookie = response.info().getheaders('Set-Cookie')
  else:
    cookie = response.info().get('Set-Cookie')
  return cookie
def _getResponseStr(res):
  if not isinstance(res,bytes):
    return res
  htmSource = res
  try:
    html=htmSource.decode("utf-8")
  except:
    try:
      html=htmSource.decode("gb18030")
    except:
      try:
        html=htmSource.decode("ISO-8859-1")
      except:
        try:
          html=htmSource.decode("ASCII")
        except:
          try:
            html=htmSource.decode("Unicode")
          except Exception as err:
            return res
  return html

def getResponseStr(res,url,ssp=None,error=False):
  html="_error_"
  if(not _checkMaintype(_getMaintype(res))):
    return res
  htmSource = decodeZip(res)
  if not isinstance(htmSource,bytes):
    htmSource = res.read()
  domain = url.split('/')[2]
  try:
    if _cache_encodings.get(domain):
      return htmSource.decode(_cache_encodings.get(domain))
    if ssp and ssp.encodings and ssp.encodings.get(domain):
      return htmSource.decode(ssp.encodings.get(domain))
    if setting_encodings.get(domain):
      return htmSource.decode(setting_encodings.get(domain))
  except:
    pass
  try:
    html=htmSource.decode("utf-8")
    _cache_encodings[domain]="utf-8"
  except:
    try:
      html=htmSource.decode("gb18030")
      _cache_encodings[domain]="gb18030"
    except:
      try:
        html=htmSource.decode("ISO-8859-1")
        _cache_encodings[domain]="ISO-8859-1"
      except:
        try:
          html=htmSource.decode("ASCII")
          _cache_encodings[domain]="ASCII"
        except:
          try:
            html=htmSource.decode("Unicode")
            _cache_encodings[domain]="Unicode"
          except Exception as err:
            if(not error):
              log(err.reason or err.message,url)
            else:
              return htmSource
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
    if headers != None:
      cookie = _getCookie(response)
      if cookie:
        headers['newCookie']=cookie
    if(ssp): 
      if(error):
        data = ssp.afterResponse(response,url,error)
      else:
        data = ssp.afterResponse(response,url)
    else: 
      data = getResponseStr(response,url,ssp,error)
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
  data={
    'url':url,
    'title':title,
    'html':html,
    'model':json.dumps(model),
    'key':extract_api_key
  }
  if(modelName): 
    data['modelName']=json.dumps(modelName)
  obj = requestPost(extract_api_url,data)
  return obj

# model=['{"Type":2}','{"Type":3}']
# print json.dumps(model)
