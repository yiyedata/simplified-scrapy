#!/usr/bin/python
#coding=utf-8

import urllib  
import urllib2,cookielib
import json
import sys,socket,random,time,re
import traceback
import spider_resource
from logPrint import logPrint,logError,getTime,saveFile
# type = sys.getfilesystemencoding()
def requestPost(url, data, headers, useIp=False,ssp=None):
  htmSource = None
  req = None
  response = None
  d=""
  head={}
  if data:
    d=data
  if headers:
    head=headers
  if(not head.get('User-Agent')):
    head['User-Agent']=random.choice(spider_resource.useragent)
  try:
    request = {
      'header':head,
      'url':url,
      'proxy':None,
      'data':d
    }
    if(ssp):
      request = ssp.beforeRequest(request)
      head = request['header']
      url = request['url']
      d = request['data']
    if(useIp and request['proxy']):
      _setProxy(request['proxy'])

    req = urllib2.Request(url, d, head)
    response = urllib2.urlopen(req,timeout=10)
    # cookie = response.info().getheaders('Set-Cookie')
    htmSource = response.read()  
  except Exception as err:
    logError(traceback.format_exc(),err,url)
    pass
  finally:
    if response:
      response.close()
  return _getResponseStr(htmSource,url)
def _getResponseStr(htmSource,url):
  html=None
  if(htmSource):
    try:
      html=htmSource.decode("utf8")
    except:
      try:
        html=htmSource.decode("gbk")
      except Exception as err:
        logError(traceback.format_exc(),err,url)
  return html
def _setProxy(proxy):
  proxyip=proxy
  # proxy_support = urllib2.ProxyHandler({'http':proxyip})
  # # nullproxy_handler = urllib2.ProxyHandler({})
  # opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
  # urllib2.install_opener(opener)
  print 'proxyip',proxyip
def dic2tuple(dic):
  tp=[]
  for key in dic:
    tp.append((key,dic[key]))
  return tp
def requestGet(url, headers, useIp, ssp=None):
  response = None
  head = {}
  if headers:
    head = headers
  if(not head.get('User-Agent')):
    head['User-Agent']=random.choice(spider_resource.useragent)
  request = {
    'header':head,
    'url':url,
    'proxy':None
  }
  request = ssp.beforeRequest(request)
  head = request['header']
  url = request['url']
  try:
    #url=url.decode("UTF-8").encode(type)
    if(useIp and request['proxy']):
      _setProxy(request['proxy'])
    cookie = cookielib.CookieJar()
    cookiehandler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(cookiehandler)
    opener.addheaders = dic2tuple(head)
    response = opener.open(url)
    data = ssp.afterResponse(response,cookie,url)
    return data
    # htmSource = response.read()
  except Exception as err:
    logError(traceback.format_exc(),err,url)
  finally:
    if response:
      response.close()

def extractHtml(url,html,model,modelName,title=None):
  headers = { "Content-Type": "application/json" }
  data={
    'url':url,
    'title':title,
    'html':html,
    'modelName':json.dumps(modelName),
    'model':json.dumps(model),
    'key':"yiyedata_test" 
  }
  data = json.dumps(data)
  # saveFile('extractHtml.txt',data)
  obj = requestPost('http://www.yiyedata.com/api/extracts',data,headers)
  return obj#.decode("UTF-8").encode(type)

def test():
  print 'start'
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
  print requestPost('http://www.yiyedata.com/api/extracts',data,headers,None)
# test()
# model=['{"Type":2}','{"Type":3}']
# print json.dumps(model)