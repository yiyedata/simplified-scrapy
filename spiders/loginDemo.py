import json
from core.spider import Spider 
from redis_urlstore import RedisUrlStore
from mongo_objstore import MongoObjStore
class LoginDemoSpider(Spider):
  # concurrencyPer1s=2
  name = 'demo-spider'
  start_urls = [{'url':'http://47.92.87.212:8080/yiye.mgt/api/push/list',
    'requestMethod':'post',
    'postData':'{"index":1,"tbName":"biaoshu","keyword":"","count":10}'}]

  # Storing URLs with redis, if you don't like this, please comment it out 
  # url_store = RedisUrlStore()
  # Storing Objs with mongodb, if you don't like this, please comment it out 
  # obj_store = MongoObjStore()

  def afterResponse(self, response, url):
    html = Spider.afterResponse(self, response, url)
    return Spider.removeScripts(self, html)
  def extract(self, url, html, models, modelNames):
    print url,models,modelNames
    if(html):
      print json.loads(html)
  def login(self):
    login_data={
      'url':'http://47.92.87.212:8080/yiye.mgt/api/pub/login',
      'headers': { 'User-Agent' : 'yazz', "Content-Type": "application/json",
        "Referer":"http://47.92.87.212:8080/yiye.mgt/view/login.jsp"
      },
      'data': {'name':'demo', 'pwd':'123456','url':'123'}
    }
    html = Spider.login(self,login_data)
    print html
    if(html):
      obj = json.loads(html)
      return obj.get('code')==1
    return False

# test=DemoSpider()
# test.login()