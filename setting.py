#!/usr/bin/python
#coding=utf-8
import logging
logging.basicConfig(
  level=logging.DEBUG,#控制台打印的日志级别
  filename='spider.log',
  filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志。a是追加模式，默认如果不写的话，就是追加模式
  format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
SETTINGFILE='setting.json'
max_workers=10
# SPIDERS=[
#   # {'file':'spiders.demoSpider','class':'DemoSpider'},
#   # {'file':'spiders.meishi_all','class':'MeishiSpider'}
#   {'file':'spiders.imageSpider','class':'ImageSpider'}
# ]
# SPIDERSPATH='spiders/'
# #并发下载线程数
# CONCURRENCY=1
# #10秒内请求页面数最大值
# CONCURRENCYPER1S=6
# #线程间隔时间
# INTERVALTIME=0.3