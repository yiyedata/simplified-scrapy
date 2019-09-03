from core.spider import Spider 
from core.redis_urlstore import RedisUrlStore
from core.mongo_objstore import MongoObjStore
class DemoSpider(Spider):
  # concurrencyPer1s=2
  name = 'demo-spider'
  start_urls = ['http://health.sina.com.cn/']
  models = ['auto_main_2','auto_obj']

  # Storing URLs with redis, if you don't like this, please comment it out 
  # url_store = RedisUrlStore(name,{'host':'127.0.0.1','port':6379})
  # Storing Objs with mongodb, if you don't like this, please comment it out 
  # obj_store = MongoObjStore(name,{'host':'127.0.0.1','port':27017})

  def afterResponse(self, response, url):
    html = Spider.afterResponse(self, response, url)
    return Spider.removeScripts(self, html)
