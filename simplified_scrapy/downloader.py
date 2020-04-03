#!/usr/bin/python
#coding=utf-8
import json,re,importlib,time
from simplified_scrapy.core.request_helper import requestPost,requestGet

# from yiye_common.module_helper import import_module
def execDownload(url,ssp):
  html = ''
  try:
    headers = url.get('header')
    if(not headers):
      headers = url.get('cookie')
    head = headers
    if(headers):
      if not isinstance(headers,dict):
        head = json.loads(headers)
    if ssp.custom_down:
      html = ssp.customDown(url)
    method = None
    if(url.get('requestMethod')):
      method = url.get('requestMethod').lower()
    if not method and url.get('method'):
      method = url.get('method').lower()

    data = url.get('postData')
    if not data:
      data = url.get('data')
    if method:
      if(method == 'post'):
        html = _requestPost(url,ssp,head,data)
      elif(method == 'custom'):
        html = ssp.customDown(url)
      elif method == 'get':
        html = _requestGet(url,ssp,head)
      else:
        html = _requestPost(url,ssp,head,data,method)
    elif data:
      html = _requestPost(url,ssp,head,data)
    else:
      html = _requestGet(url,ssp,head)
    if head: url['header'] = head #json.dumps(head)
  except Exception as err:
    print (err)
  return html

def _requestPost(url,ssp,header,data,method=None):
  if(url.get('request_timeout')):
    return requestPost(url['url'],data,header,url.get('useIp')==1,ssp,url.get('request_timeout'),method=method)
  elif(ssp.request_timeout):
    return requestPost(url['url'],data,header,url.get('useIp')==1,ssp,ssp.request_timeout,method=method)
  else:
    return requestPost(url['url'],data,header,url.get('useIp')==1,ssp,method=method)

def _requestGet(url,ssp,header):
  if(url.get('request_timeout')):
    return requestGet(url['url'],header,url.get('useIp')==1,ssp,url.get('request_timeout'))
  elif(ssp.request_timeout):
    return requestGet(url['url'],header,url.get('useIp')==1,ssp,ssp.request_timeout)
  else:
    return requestGet(url['url'],header,url.get('useIp')==1,ssp)