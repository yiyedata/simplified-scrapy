# simplified-scrapy
simplified scrapy, A Simple Web Crawle
# Requirements
+ Python 2.7, 3.0+
+ Works on Linux, Windows, Mac OSX, BSD
# 运行
进入项目根目录，执行下面命令  
`python start.py`
# Demo
项目中爬虫例子，在文件夹spiders下，文件名为demoSpider.py。自定义的爬虫类需要继承Spider类
```
from core.spider import Spider 
class DemoSpider(Spider):
```
需要给爬虫定义一个名字，配置入口链接地址，与抽取数据用到的解析方法。下面是采集数据的一个例子。
```
from simplified_scrapy.core.spider import Spider 
from simplified_scrapy.simplified_doc import SimplifiedDoc
class DemoSpider(Spider):
  name = 'demo-spider'
  start_urls = ['http://www.scrapyd.cn/']
  allowed_domains = ['www.scrapyd.cn']
  def extract(self, url, html, models, modelNames):
    doc = SimplifiedDoc(html)
    lstA = doc.listA(url=url["url"])
    return [{"Urls": lstA, "Data": None}]

from simplified_scrapy.simplified_main import SimplifiedMain
SimplifiedMain.startThread(DemoSpider())
```

# pip安装
```
pip install simplified-scrapy
```
[Examples](https://github.com/yiyedata/simplified-scrapy-demo)



