#!/usr/bin/python
#coding=utf-8
from core.spider import Spider 
from core.redis_urlstore import RedisUrlStore
from core.mongo_objstore import MongoObjStore
from core.mongo_htmlstore import MongoHtmlStore
from core.mongo_urlstore import MongoUrlStore
from core.sqlite_htmlstore import SqliteHtmlStore
# from meishi_urlstore import MeishiUrlStore
class MeishiSpider(Spider):
  # concurrencyPer1s=2
  name = 'meishi-test-spider'
  # start_urls = ['https://www.meishichina.com/Health/','https://www.meishij.net/jiankang/']
  models = ['auto_main','auto_obj']
  # start_urls = ['http://www.sohu.com/tag/19580?spm=smpc.chihe-home.side-nav.19.1567069809060ucSUkxO'
  #   'http://chihe.sohu.com/','http://www.sohu.com/tag/19581?spm=smpc.chihe-home.side-nav.15.1567069809060ucSUkxO',
  #   'http://www.sohu.com/tag/68062?spm=smpc.chihe-home.side-nav.17.1567069809060ucSUkxO',
  #   'http://www.sohu.com/tag/68060?spm=smpc.chihe-home.side-nav.16.1567069809060ucSUkxO',
  #   'http://www.sohu.com/tag/19577?spm=smpc.chihe-home.side-nav.24.1567069809060ucSUkxO',
  #   'http://www.sohu.com/tag/20846?spm=smpc.chihe-home.side-nav.29.1567069809060ucSUkxO',
  #   'http://www.sohu.com/tag/22547?spm=smpc.chihe-home.side-nav.32.1567069809060ucSUkxO',
  #   'http://www.sohu.com/tag/77843?spm=smpc.tag-page.hot-spots.6.1567070531038i5uDqXS']
  # start_urls = ['https://www.douguo.com/','https://www.meishic.com/','http://edu.sina.com.cn/zl/eat/','http://www.ttmeishi.com/']
  start_urls = ['http://www.someishi.com/recipe/category/']
  # 'https://www.xinshipu.com/zuofa/788340','http://www.jiaodong.net/food/'
  # Storing URLs with redis, if you don't like this, please comment it out 
  # url_store = RedisUrlStore()
  # Storing Objs with mongodb, if you don't like this, please comment it out 
  obj_store = MongoObjStore(name)
  html_store = SqliteHtmlStore(name)
  url_store = MongoUrlStore(name)

  def extract(self, url, html, models, modelNames):
    if(url.get('title') and len(url.get("title"))<3):
      url['title']=''
    # if(url.find('')>0):
    obj = Spider.extract(self,url,html,models,modelNames)
    return obj

  def afterResponse(self, response, url):
    html = Spider.afterResponse(self, response, url)
    return Spider.removeScripts(self, html)

  def urlFilter(self,url):
    if(url.find('Health/')>0 or url.find('jiankang/')>0 
        or url.find('xinxianzixun')>0 or url.find('shipinanquan')>0 
        or url.find('wenhua')>0 or url.find('yangsheng')>0 or url.find('zuofa')>0
        or url.find('/a/')>0 or url.find('tag/19581')>0 or url.find('tag/19580')>0
        or url.find('tag/68062')>0 or url.find('tag/68060')>0 or url.find('tag/19577')>0
        or url.find('tag/20846')>0 or url.find('tag/22547')>0 or url.find('tag/77843')>0
        or url.find('chihe.sohu')>0
        or url.find('douguo.com')>0 or url.find('meishic.com/')>0 or url.find('zl/eat/')>0
        or url.find('ttmeishi.com')>0
        or url.find('someishi.com')>0):
        # 'tag/68062,68060,19577,20846,22547,77843'
        if(url.find('/Video')>0): return False
        return True
    return False
