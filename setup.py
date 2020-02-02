#!/usr/bin/python
# -*- coding: UTF-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplified_scrapy",
    version="1.0.111",
    author="yiyedata",
    author_email="3095069599@qq.com",
    description="A Simple Distributed Web Crawle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yiyedata/simplified-scrapy",
    packages=setuptools.find_packages(include=["simplified_scrapy","simplified_scrapy.core",
        "simplified_html"
    ]),
    include_package_data=True,    # 自动打包文件夹内所有数据
    zip_safe=True,                # 设定项目包为安全，不用每次都检测其安全性
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
