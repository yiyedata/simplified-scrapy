#!/usr/bin/python
#coding=utf-8
class CookieStoreBase:
  def getCookie(self, url):
    raise NotImplementedError

  def setCookie(self, url, cookie):
    raise NotImplementedError
  