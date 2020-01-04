#!/usr/bin/python
#coding=utf-8
import os,io,json,time
import sqlite3
import sys
from simplified_scrapy.core.utils import printInfo,getTimeNow,md5
  
class SqliteHtmlStore:
  # _htmls=[]
  _htmlPath='htmls/{}/'
  _dbPath='db/{}.db'
  _tbName='htmls'
  def __init__(self, name):
    try:
      self._htmlPath = self._htmlPath.format(name)
      if(not os.path.exists('db/')):
        os.mkdir('db/')
      if(not os.path.exists('htmls/')):
        os.mkdir('htmls/')
      if(not os.path.exists(self._htmlPath)):
        os.mkdir(self._htmlPath)
      self._dbPath = self._dbPath.format(name)
      conn = sqlite3.connect(self._dbPath)
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS htmls
            (id INTEGER PRIMARY KEY autoincrement,
            json  TEXT  NOT NULL,
            state INT NOT NULL DEFAULT 0,
            tm  TEXT);''')
      conn.commit()
      conn.close()
    except Exception as err:
      printInfo(err)
  
  # def __del__(self):
  #   if self._conn: self._conn.close()

  def saveHtml(self,url,html):
    if(not isinstance(url,dict)):
      url={"url":url}
    filename = self._saveHtml(url["url"],html)
    # self._htmls.append({"url":url,"html":html})
    conn = sqlite3.connect(self._dbPath)
    conn.cursor().execute("INSERT INTO htmls (json,state,tm) VALUES (?,?,?)",(json.dumps({"url":url,"html":filename}),0, getTimeNow()))
    conn.commit() 
    conn.close()

  def popHtml(self,state=0):
    conn = sqlite3.connect(self._dbPath)
    cursor = conn.cursor().execute("select id,json from htmls where state="+str(state)+" limit 0,1")
    for row in cursor:
      obj=json.loads(row[1])
      obj['id']=row[0]
      obj['html']=io.open(self._htmlPath+obj['html'], "r",encoding="utf-8").read()#.encode("utf-8")
      return obj
    conn.close()

  def _saveHtml(self,url,html):
    suffix = '.htm'
    index = url.rfind('/')
    if(index>10):
      index = url.rfind('.',index)
      if(index>0 and len(url)-index<10):
        suffix = url[index:]
    filename = md5(url)+suffix
    if(not os.path.exists(self._htmlPath)):
      os.mkdir(self._htmlPath)
    file = io.open(self._htmlPath+filename, "w",encoding="utf-8")
    file.write(html)
    file.close()
    return filename

  def updateState(self,id,state):
    conn = sqlite3.connect(self._dbPath)
    conn.cursor().execute("update htmls set state=? where id=?", (state, id)) 
    conn.commit()
    conn.close()