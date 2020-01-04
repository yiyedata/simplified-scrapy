#!/usr/bin/python
#coding=utf-8
import pymssql,json
class MssqlObjStore:
  _host='(local)'
  _port=1433
  _user='sa'
  _pwd='12345678'
  _dbName = 'simplified_scrapy_db'
  _tbName = 'obj_'
  def __init__(self, name, setting=None):
    self._tbName = self._tbName + name.replace('-','_')
    if(setting):
      if(setting.get('server')):
        self._host=setting.get('server')
      if(setting.get('host')):
        self._host=setting.get('host')
      if(setting.get('port')):
        self._port=setting.get('port')
      if(setting.get('user')):
        self._user=setting.get('user')
      if(setting.get('dbName')):
        self._dbName=setting.get('dbName')
      if(setting.get('tbName')):
        self._tbName=setting.get('tbName')
      if(setting.get('password')):
        self._pwd=setting.get('password')
    # conn = None
    # try:
    #   conn = self._connect()
    #   cursor = conn.cursor()
    #   cursor.execute("""
    #   IF OBJECT_ID('{}', 'U') IS NULL
    #     CREATE TABLE {} (
    #         id INT identity(1,1),
    #         json TEXT,
    #         addTime DATETIME DEFAULT GETDATE(),
    #         PRIMARY KEY(id)
    #     )""".format(self._dbName))
    #   conn.commit()
    # except Exception as err:
    #   print (err)
    # if conn:
    #   conn.close()

  def connect(self):
    conn = pymssql.connect(self._host, self._user, self._pwd, self._dbName)
    return conn

  def saveObj(self, data):
    conn = None
    objs = data.get("Datas")
    if(objs != None):
      if(not objs): return
    elif not isinstance(data, dict): return
    try:
      conn = self.connect()
      cursor = conn.cursor()
      cursor.execute("insert into [{}]([json]) values(%s)".format(self._tbName),(json.dumps(data)))
      conn.commit()
    except Exception as err:
      print (err)
    if conn:
      conn.close()