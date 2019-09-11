#!/usr/bin/python
#coding=utf-8
import json,hashlib,random,sqlite3,logging
from utils import getTimeNow,printInfo
class SqliteUrlStore():
  _dbPath = 'db/{}.db'
  _tbName = 'urls'
  def log(self, msg, level=logging.ERROR):
    printInfo(msg)
    logger = logging.getLogger()
    logging.LoggerAdapter(logger, None).log(level, msg)

  def __init__(self,name):
    self._dbPath = self._dbPath.format(name)
    conn = sqlite3.connect(self._dbPath)
    try:
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS urls
            (id TEXT  NOT NULL,
            json  TEXT  NOT NULL,
            state INT NOT NULL DEFAULT 0,
            tm  TEXT);''')
      conn.commit()
    except Exception as err:
      self.log(err)
    conn.close()

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
    conn = sqlite3.connect(self._dbPath)
    try:
      id = hashlib.md5(url).hexdigest()
      cursor = conn.cursor().execute("select id from urls where id='{}' limit 0,1".format(id))
      flag=False
      for row in cursor:
        flag = True
    except Exception as err:
      self.log(err)
    conn.close()
    return flag

  def saveUrl(self, urls):
    datas=[]
    for url in urls:
      if(isinstance(url,str)):
        id = hashlib.md5(url).hexdigest()
        url={'url':url}
      else:
        id = hashlib.md5(url["url"]).hexdigest()
      if(not self.checkUrl(url["url"])):
        datas.append((id,json.dumps(url),getTimeNow()))
    if not len(datas): return
    conn = sqlite3.connect(self._dbPath)
    try:
      cursor = conn.cursor()
      # tmp = tuple(datas)
      cursor.executemany("insert into urls(id,json,state,tm) values(?,?,0,?)",tuple(datas))
      conn.commit()
    except Exception as err:
      self.log(err)
    conn.close()

  def resetUrls(self, urls):
    datas=[]
    for url in urls:
      if(isinstance(url,str)):
        id = hashlib.md5(url).hexdigest()
        url={'url':url}
      else:
        id = hashlib.md5(url["url"]).hexdigest()
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