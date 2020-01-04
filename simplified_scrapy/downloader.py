#!/usr/bin/python
#coding=utf-8
import json,re,importlib
from simplified_scrapy.core.request_helper import requestPost,requestGet

# from yiye_common.module_helper import import_module
def execDownload(url,ssp):
  headers = url.get('header')
  if(not headers):
    headers = url.get('cookie')
  head=None
  if(headers):
    head=json.loads(headers)
  if ssp.custom_down:
    return ssp.customDown(url)
  if(url.get('requestMethod')):
    method = url.get('requestMethod').lower()
    if(method == 'post'):
      return _requestPost(url,ssp,head)
    # elif(method == 'render'):
    #   return ssp.renderUrl(url)
    elif(method == 'custom'):
      return ssp.customDown(url)
  return _requestGet(url,ssp,head)

def _requestPost(url,ssp,header):
  if(url.get('request_timeout')):
    return requestPost(url['url'],url.get('postData'),header,url.get('useIp')==1,ssp,url.get('request_timeout'))
  elif(ssp.request_timeout):
    return requestPost(url['url'],url.get('postData'),header,url.get('useIp')==1,ssp,ssp.request_timeout)
  else:
    return requestPost(url['url'],url.get('postData'),header,url.get('useIp')==1,ssp)

def _requestGet(url,ssp,header):
  if(url.get('request_timeout')):
    return requestGet(url['url'],header,url.get('useIp')==1,ssp,url.get('request_timeout'))
  elif(ssp.request_timeout):
    return requestGet(url['url'],header,url.get('useIp')==1,ssp,ssp.request_timeout)
  else:
    return requestGet(url['url'],header,url.get('useIp')==1,ssp)