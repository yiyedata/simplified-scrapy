from core.spider import Spider 
from redis_urlstore import RedisUrlStore
from mongo_objstore import MongoObjStore
class DemoSpider(Spider):
  # concurrencyPer1s=2
  name = 'demo-spider'
  start_urls = ['http://health.sina.com.cn/']
  models = ['auto_main_2','auto_obj']

  # Storing URLs with redis, if you don't like this, please comment it out 
  # url_store = RedisUrlStore()
  # Storing Objs with mongodb, if you don't like this, please comment it out 
  # obj_store = MongoObjStore()

  def afterResponse(self, response, url):
    html = Spider.afterResponse(self, response, url)
    return Spider.removeScripts(self, html)
