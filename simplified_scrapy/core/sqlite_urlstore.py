#!/usr/bin/python
#coding=utf-8
import json,random,sqlite3,logging,os
import sys
from simplified_scrapy.core.utils import printInfo,getTimeNow,md5
from simplified_scrapy.core.urlstore_base import UrlStoreBase
  
class SqliteUrlStore(UrlStoreBase):
  _dbPath = 'db/{}.db'
  _tbName = 'urls'
  _duplicateRemoval = True
  def log(self, msg, level=logging.ERROR):
    printInfo(msg)
    logger = logging.getLogger()
    logging.LoggerAdapter(logger, None).log(level, msg)

  def __init__(self,name, setting=None):#,duplicateRemoval=True):
    if(not os.path.exists('db/')):
      os.mkdir('db/')
    if setting and setting.get('duplicateRemoval')!=None:
      self._duplicateRemoval = setting.get('duplicateRemoval')
    self._dbPath = self._dbPath.format(name)
    conn = None
    try:
      conn = sqlite3.connect(self._dbPath)
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS urls
            (id TEXT PRIMARY KEY NOT NULL,
            json TEXT NOT NULL,
            state INT NOT NULL DEFAULT 0,
            tm  TEXT);''')
      # if duplicateRemoval:
      #   c.execute('''CREATE TABLE IF NOT EXISTS dic
      #         (id TEXT PRIMARY KEY NOT NULL);''')
      conn.commit()
    except Exception as err:
      self.log(err)
    if (conn): conn.close()

  def popUrl(self):
    conn = sqlite3.connect(self._dbPath)
    url=None
    try:
      cursor = conn.cursor().execute("select id,json from urls where state=0 limit 0,1")
      for row in cursor:
        url=json.loads(row[1])
        id=row[0]

      if(url): 
        conn.cursor().execute("update urls set state=1 where id='{}'".format(id))
        conn.commit()
    except Exception as err:
      self.log(err)
    conn.close()
    return url

  def getCount(self):
    conn = sqlite3.connect(self._dbPath)
    try:
      cursor = conn.cursor().execute("select count(id) from urls where state=0")
      count=0
      for row in cursor:
        count = row[0]
    except Exception as err:
      self.log(err)
    conn.close()
    return count

  def checkUrl(self,url):
    if not self._duplicateRemoval: return False
    conn = sqlite3.connect(self._dbPath)
    try:
      flag=False
      id = md5(url)
      cursor = conn.cursor().execute("select id from urls where id='{}' limit 0,1".format(id))
      for row in cursor:
        flag = True
    except Exception as err:
      self.log(err)
    conn.close()
    return flag

  def saveUrl(self, urls,i=None):
    datas=[]
    for url in urls:
      if(not isinstance(url,dict)):
        id = md5(url)
        url={'url':url}
      else:
        id = md5(url["url"])
      if(not self.checkUrl(url["url"])):
        datas.append((id,json.dumps(url),getTimeNow()))
    if not datas: return
    conn = sqlite3.connect(self._dbPath)
    try:
      cursor = conn.cursor()
      # tmp = tuple(datas)
      cursor.executemany("REPLACE into urls(id,json,state,tm) values(?,?,0,?)",tuple(datas))
      conn.commit()
    except Exception as err:
      self.log(err)
    conn.close()

  def clearUrl(self):
    conn = sqlite3.connect(self._dbPath)
    flag = False
    try:
      conn.cursor().execute("DELETE from urls")
      conn.commit()
    except Exception as err:
      self.log(err)
    conn.close()
    return flag
  def resetUrls(self, urls):
    datas=[]
    for url in urls:
      if(not isinstance(url,dict)):
        id = md5(url)
        url={'url':url}
      else:
        id = md5(url["url"])
      datas.append((id,json.dumps(url),getTimeNow()))
    if not len(datas): return
    conn = sqlite3.connect(self._dbPath)
    try:
      cursor = conn.cursor()
      # tmp = tuple(datas)
      cursor.executemany("REPLACE into urls(id,json,state,tm) values(?,?,0,?)",tuple(datas))
      conn.commit()
    except Exception as err:
      self.log(err)
    conn.close()
  def updateState(self, url, state):
    conn = sqlite3.connect(self._dbPath)
    try:
      if(not isinstance(url,dict)):
        id = md5(url)
      else:
        id = md5(url["url"])
      conn.cursor().execute("update urls set state={} where id='{}'".format(state, id))
      conn.commit()
    except Exception as err:
      self.log(err)
    conn.close()