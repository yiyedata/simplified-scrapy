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
需要给爬虫定义一个名字，配置入口链接地址，与抽取数据用到的模型名称。下面是采集新浪健康资讯数据的一个例子。其中auto_main_2表示抽取相同2级域名的链接，auto_obj表示自动抽取页面中的资讯数据，包括标题、正文和时间。
```
name = 'demo-spider'
start_urls = ['http://health.sina.com.cn/']
models = ['auto_main_2','auto_obj']
```
其中模型文件在文件夹models下，如果需要自定义模型，可以使用这个模型工具，[下载地址](https://github.com/yiyedata/yiyespider/raw/master/publish/yiyeclient_0.9.zip)。使用说明在[这里](https://github.com/yiyedata/yiyespider/raw/master/%E4%B8%80%E4%B8%9A%E5%88%86%E5%B8%83%E5%BC%8F%E9%80%9A%E7%94%A8%E9%87%87%E9%9B%86%E7%B3%BB%E7%BB%9F%E6%A8%A1%E5%9E%8B%E5%B7%A5%E5%85%B7%E6%96%87%E6%A1%A3.docx)

# pip安装
```
pip install simplified-scrapy
```
[例子](https://github.com/yiyedata/simplified-scrapy-demo)

