#coding=utf-8
import time,json
from pymongo import MongoClient
from core.request_helper import requestPost
class MongoObjStore:
  _host='192.168.31.202'
  _port=27017
  _dbName='python_db'
  _tbName='obj_'
  
  _appSecret = "123456789"
  _appId = 'python-export'
  _url = "http://47.92.87.212:8080/yiye.mgt/api/client"
  # _key='yiyedata_test'
    
  def __init__(self, name):
    self._tbName = self._tbName + name
  def _connect(self):
    conn = MongoClient(self._host, self._port)
    return conn[self._dbName]

  def exportObj(self):
      db = self._connect()
      while True:
        objs = db[self._tbName].find({"state":{ "$exists": False }})
        if not objs:
          objs = db[self._tbName].find({"state":-2})
        if objs:
          for obj in objs:
            try:
              id = obj["_id"]
              result = self._exportObj(obj)
              db[self._tbName].update({"_id": id}, {"$set": {"state": result}})
              time.sleep(0.3)
            except Exception as err:
              print err
        else:
          time.sleep(100)
        time.sleep(5)

  def _exportObj(self,data):
    if(data["Datas"][0]["Value"][-1:]=="。"):
      return
    print data["_id"]
    del data["_id"]
    del data["Json"]
    data["Time"]= time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    body = {"id":self._appId, "appSecret":self._appSecret, 'objs':[data], 
    "type":"objs", "tbName":"objDefault", "mongoDb":"mongodb://127.0.0.1:3317;MeishiDb"}
 
    result = requestPost(self._url, json.dumps(body),{ "Content-Type": "application/json"})
    if(result):
      obj = json.loads(result)
      return obj.get('code')
    print result
    return -2

test = MongoObjStore('meishi-test-spider')
test.exportObj()