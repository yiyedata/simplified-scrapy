import json
from core.spider import Spider 
# from redis_urlstore import RedisUrlStore
# from mongo_objstore import MongoObjStore
class LoginDemoSpider(Spider):
  # concurrencyPer1s=2
  name = 'sina-spider'
  models = ['auto_obj']
  # start_urls = [{'url':'http://api.search.sina.com.cn/?c=news&t=&q=%E7%BE%8E%E9%A3%9F&pf=0&ps=0&page=3&stime=2018-08-24&etime=2019-08-26&sort=rel&highlight=1&num=10&ie=utf-8&callback=jQuery17207169526774405917_1566706122236&_=1566706215414',
  #   'requestMethod':'post',
  #   'postData':'{"index":1,"tbName":"biaoshu","keyword":"","count":10}'}]

  # Storing URLs with redis, if you don't like this, please comment it out 
  # url_store = RedisUrlStore()
  # Storing Objs with mongodb, if you don't like this, please comment it out 
  # obj_store = MongoObjStore()

  def afterResponse(self, response, url):
    html = Spider.afterResponse(self, response, url)
    return Spider.removeScripts(self, html)
  def extract(self, url, html, models, modelNames):
    if(html and html[0:6]=='jQuery'):
      index = html.find('{')
      lines = json.loads(html[index:-1])
      urls = []
      for line in lines['list']:
        urls.append({'title':line['title'],'url':line['url']})
      self.saveUrl(urls)
      return False
      # print json.loads(html)
    return True
  def login(self):
    login_data={
      'url':'http://www.sina.com.cn/mid/search.shtml?range=all&c=news&q=%E7%BE%8E%E9%A3%9F&from=home&ie=utf-8',
      'headers': { 'Cookie': 'UOR=,www.sina.com.cn,; U_TRS1=00000058.d6c8bf.5d620e05.e9f118b7; U_TRS2=00000058.d6cfbf.5d620e05.9591e146; SGUID=1566707205033_19514325; SINAGLOBAL=120.244.142.88_1566707206.17598; Apache=120.244.142.88_1566707206.17600; ULV=1566707205945:1:1:1:120.244.142.88_1566707206.17600:; lxlrttp=1560672234; SUB=_2AkMqPoE4f8PxqwJRmPoXzWvqaIV3ywjEieKcYnDjJRMyHRl-yD8XqhIztRB6Ab6v10Nx_DkWmF_LIVFq2lieDOwW3ivV; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFS0E0mR_3GYCER3CwSGN2-'
      },
      'method':'get'
    }
    html = Spider.login(self,login_data)
    urls = []
    i=0
    while(i<10):
      urls.append(u'http://api.search.sina.com.cn/?c=news&t=&q=\u7f8e\u98df&pf=0&ps=0&page='+str(i)+'&stime=2018-08-24&etime=2019-08-26&sort=rel&highlight=1&num=10&ie=utf-8&callback=jQuery172029476581133638624_1566707330011&_=1566708696875')
      i=i+1
    self.saveUrl(urls)
    # print html
    # if(html):
    #   obj = json.loads(html)
    #   return obj.get('code')==1
    return True

# test=DemoSpider()
# test.login()
