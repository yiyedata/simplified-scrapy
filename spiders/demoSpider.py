from simplified_scrapy.spider import Spider 
class DemoSpider(Spider):

  name = 'demo-spider'
  start_urls = ['http://www.scrapyd.cn/']
  models = ['auto_main_2','auto_obj']

  
  # from simplified_scrapy.core.redis_urlstore import RedisUrlStore
  # from simplified_scrapy.core.mongo_objstore import MongoObjStore
  # Storing URLs with redis, if you don't like this, please comment it out 
  # url_store = RedisUrlStore(name,{'host':'127.0.0.1','port':6379})
  # Storing Objs with mongodb, if you don't like this, please comment it out 
  # obj_store = MongoObjStore(name,{'host':'127.0.0.1','port':27017})

  def afterResponse(self, response, url):
    html = Spider.afterResponse(self, response, url)
    return Spider.removeScripts(self, html)
from simplified_scrapy.simplified_main import SimplifiedMain
SimplifiedMain.startThread(DemoSpider())