from core.spider import Spider 
from redis_urlstore import RedisUrlStore
from mongo_objstore import MongoObjStore
from mongo_htmlstore import MongoHtmlStore
from meishi_urlstore import MeishiUrlStore
class MeishiSpider(Spider):
  # concurrencyPer1s=2
  name = 'meishi-spider'
  start_urls = ['https://www.meishichina.com/Health/','https://www.meishij.net/jiankang/']
  models = ['auto_main','auto_obj']

  # Storing URLs with redis, if you don't like this, please comment it out 
  # url_store = RedisUrlStore()
  # Storing Objs with mongodb, if you don't like this, please comment it out 
  obj_store = MongoObjStore(name)
  html_store = MongoHtmlStore(name)
  url_store = MeishiUrlStore(name)

  def extract(self, url, html, models, modelNames):
    if(url.get('title') and len(url.get("title"))<3):
      url['title']=''
    obj = Spider.extract(self,url,html,models,modelNames)
    return obj

  def afterResponse(self, response, url):
    html = Spider.afterResponse(self, response, url)
    return Spider.removeScripts(self, html)
