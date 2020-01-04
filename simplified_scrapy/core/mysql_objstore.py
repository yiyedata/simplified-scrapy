#!/usr/bin/python
#coding=utf-8
import pymysql,json
class MysqlObjStore:
  _host='127.0.0.1'
  _port=3306
  _user='root'
  _pwd='root'
  _dbName = 'simplified_scrapy_db'
  _tbName = 'obj_'
  _charset = 'utf8mb4'
  def __init__(self, name, setting=None):
    self._tbName = self._tbName + name.replace('-','_')
    if(setting):
      if(setting.get('server')):
        self._host=setting.get('server')
      if(setting.get('host')):
        self._host=setting.get('host')
      if(setting.get('user')):
        self._user=setting.get('user')
      if(setting.get('dbName')):
        self._dbName=setting.get('dbName')
      if(setting.get('tbName')):
        self._tbName=setting.get('tbName')
      if(setting.get('pwd')):
        self._pwd=setting.get('pwd')
      if(setting.get('port')):
        self._port=setting.get('port')
      if(setting.get('charset')):
        self._charset=setting.get('charset')

  def connect(self):
    return pymysql.connect(host=self._host, port=self._port, user=self._user, 
                            password=self._pwd, database=self._dbName,
                            charset=self._charset)

  def saveObj(self, data):
    conn = None
    cur = None
    objs = data.get("Datas")
    if(objs != None):
      if(not objs): return
    elif not isinstance(data, dict): return
    try:
      conn = self.connect()
      cur = conn.cursor()
      try:
        cur.execute("insert into {}(json) values(%s)".format(self._tbName),(json.dumps(data)))
        return conn.commit()
      except Exception as err:
        conn.rollback()
        print (err)
    except Exception as err:
      print (err)
    finally:
      if(cur): cur.close()
      if(conn): conn.close()