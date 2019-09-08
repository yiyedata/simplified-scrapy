#!/usr/bin/python
#coding=utf-8
import os,io,hashlib,json,time
import sqlite3
from utils import getTimeNow
class SqliteHtmlStore:
  # _htmls=[]
  _htmlPath='htmls/{}/'
  _dbPath='db/{}.db'
  _tbName='htmls'
  def __init__(self, name):
    self._htmlPath = self._htmlPath.format(name)
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
  
  # def __del__(self):
  #   if self._conn: self._conn.close()

  def saveHtml(self,url,html):
    if(isinstance(url,str)):
      url={"url":url}
    filename = self._saveHtml(url["url"],html)
    # self._htmls.append({"url":url,"html":html})
    conn = sqlite3.connect(self._dbPath)
    conn.cursor().execute("INSERT INTO htmls (json,state,tm) VALUES (?,?,?)",(json.dumps({"url":url,"html":filename}),0, getTimeNow()))
    conn.commit() 
    conn.close()

  def popHtml(self):
    # if(len(self._htmls)>0):
    #   return self._htmls.pop()
    conn = sqlite3.connect(self._dbPath)
    cursor = conn.cursor().execute("select id,json from htmls where state=0 limit 0,1")
    for row in cursor:
      obj=json.loads(row[1])
      obj['id']=row[0]
      obj['html']=io.open(self._htmlPath+obj['html'], "r",encoding="utf-8").read()#.encode("utf-8")
      return obj
    conn.close()

  def _saveHtml(self,url,html):
    filename = hashlib.md5(url).hexdigest()+'.htm'
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