#!/usr/bin/python
#coding=utf-8
import json,re,importlib
from spiders.core.request_helper import requestPost,requestGet
# from yiye_common.module_helper import import_module
def execDownload(url,ssp):
  headers = url.get('cookie')
  head=None
  if(headers):
    head=json.loads(headers)
  if(url.get('requestMethod') and url.get('requestMethod').lower()=='post'):
    return requestPost(url['url'],url.get('postData'),head,url.get('useIp')==1,ssp)
  else:
    return requestGet(url['url'],head,url.get('useIp')==1,ssp)
