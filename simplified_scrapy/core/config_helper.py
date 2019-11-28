#!/usr/bin/python
#coding=utf-8
import json,sqlite3,logging,time,os
import sys
from simplified_scrapy.core.utils import printInfo
class ConfigHelper():
  _dbPath = 'db/config.db'
  _tbName = 'configs'
  def log(self, msg, level=logging.ERROR):
    printInfo(msg)
    logger = logging.getLogger()
    logging.LoggerAdapter(logger, None).log(level, msg)

  def __init__(self):
    conn = None
    try:
      if(not os.path.exists('db/')):
        os.mkdir('db/')
      conn = sqlite3.connect(self._dbPath)
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS configs
            (key TEXT PRIMARY KEY NOT NULL,
            value TEXT NOT NULL,
            tm TEXT);''')
      conn.commit()
    except Exception as err:
      self.log(err)
    if (conn): conn.close()

  def getValue(self,key):
    conn = sqlite3.connect(self._dbPath)
    v=None
    try:
      value = tuple([key])
      cursor = conn.cursor().execute("select `value` from configs where `key`=?",value)
      for row in cursor:
        v = row[0]
    except Exception as err:
      self.log(err)
    conn.close()
    return v

  def getValueTime(self,key):
    conn = sqlite3.connect(self._dbPath)
    v=None
    t=None
    try:
      value = tuple([key])
      cursor = conn.cursor().execute("select `value`,`tm` from configs where `key`=?",value)
      for row in cursor:
        v = row[0]
        t = float(row[1])
    except Exception as err:
      self.log(err)
    conn.close()
    return (v,t)
  def getInt(self,key):
    value = self.getValue(key)
    if(value):
      return int(value)
    return None

  def setValue(self, key, value):
    conn = sqlite3.connect(self._dbPath)
    try:
      cursor = conn.cursor()
      cursor.execute("REPLACE into configs(`key`,`value`,`tm`) values(?,?,?)",(key,value,time.time()))
      conn.commit()
    except Exception as err:
      self.log(err)
    conn.close()
Configs = ConfigHelper()