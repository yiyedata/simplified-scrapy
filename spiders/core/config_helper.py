#!/usr/bin/python
#coding=utf-8
import json,sqlite3,logging
from utils import getTimeNow,printInfo
class ConfigHelper():
  _dbPath = 'db/config.db'
  _tbName = 'configs'
  def log(self, msg, level=logging.ERROR):
    printInfo(msg)
    logger = logging.getLogger()
    logging.LoggerAdapter(logger, None).log(level, msg)

  def __init__(self):
    conn = sqlite3.connect(self._dbPath)
    try:
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS configs
            (key TEXT PRIMARY KEY NOT NULL,
            value TEXT NOT NULL);''')
      conn.commit()
    except Exception as err:
      self.log(err)
    conn.close()

  def getValue(self,key):
    conn = sqlite3.connect(self._dbPath)
    v=None
    try:
      cursor = conn.cursor().execute("select `value` from configs where `key`=?",tuple(key))
      for row in cursor:
        v = row[0]
    except Exception as err:
      self.log(err)
    conn.close()
    return v
  def getInt(self,key):
    value = self.getValue(key)
    if(value):
      return int(value)
    return None

  def setValue(self, key, value):
    conn = sqlite3.connect(self._dbPath)
    try:
      cursor = conn.cursor()
      cursor.executemany("insert into configs(`key`,`value`) values(?,?)",(key,value))
      conn.commit()
    except Exception as err:
      self.log(err)
    conn.close()
Configs = ConfigHelper()