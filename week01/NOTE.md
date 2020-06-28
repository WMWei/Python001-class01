# Week01学习笔记

本周通过对“爬取豆瓣影评”项目的学习和练习，初步了解了爬虫的运作方式，及如何通过python编写爬虫代码；学习了常用的python库和框架。  

## 1. 页面下载相关

常用的用于访问网络资源的库有：  

- `urllib`：python的标准库  

```python
from urllib import request

# GET 方法
resp = request.urlopen('http://httpbin.org/get')
# POST 方法
resp = request.urlopen('http://httpbin.org/post', data=b'key=value', timeout=10)

# cookie
from http import cookiejar
# 创建一个cookiejar对象
cookie = cookiejar.CookieJar()
# 创建cookie处理器
handler = request.HTTPCookieProcessor(cookie)
# 创建Opener对象
opener = request.build_opener(handler)
# 使用opener来发起请求
resp = opener.open('http://www.baidu.com')
# 查看之前的cookie对象，则可以看到访问百度获得的cookie
for i in cookie:
    print(i)
# 之后使用urlopen方法发起请求时，都会带上这个cookie
```

- `requests`：比内置的`urllib`库更实用且方便的第三方库  

```python
# 使用requests库获取豆瓣影评

import requests

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
header = {'user-agent':user_agent}
myurl = 'https://movie.douban.com/top250'
response = requests.get(myurl,headers=header)
```

## 2. 页面解析相关

常用的解析库：`bs4`、`lxml`  

例子：

```python
from bs4 import BeautifulSoup as bs
from lxml import etree

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

# bs方式解析
# 解析得到bs对象
soup = bs(html_doc, 'html.parser')
# 搜索并返回所有a标签的内容
soup.find_all('a')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
soup.find('a', attrs={'id': 'link1'}).text
#Elsie

# xpath方式解析
selector = etree.HTML(html.doc)

story = selector.xpath('//p[@class="story"]')
a = story[0].xpath('a/text()')
# ['Elsie', 'Lacie', 'Tillie']
elsie = a[0]
```

## 3. 数据存储相关

- 爬取到的数据可以直接通过`open('path/to/file', 'w')`写入文件中  
- 可以通过`pandas`库的数据帧`DataFrame`进行格式化，然后存储，比如存储到csv：

```python
import pandas as pd


movies = [
    ['天气之子', '2019-11-01', '爱情/动画/奇幻'],
    ['误杀', '2019-12-13', '剧情/犯罪']
]
# 格式化
movie_df = pd.DataFrame(movies, columns=['片名', '上映日期', '类型'])
# 存储到csv
movie_df.to_csv('movies.csv', encoding='utf-8', index=Fasle)
```

- 还可以存储为json格式
- 可以存储到数据库中

## 4. 爬虫框架Scrapy

Scrapy是一个python实现的爬取网站数据，提取结构性数据而编写的应用框架。包括几部分：

- 引擎Engine：负责爬虫、管道、下载器、调度器等中间的通讯、数据传递；  
- 调度器Scheduler：接收引擎发出的请求，按顺序压入队列和去重；  
- 下载器Downloader：像目标URL发出请求，并将下载的网页内容返回给爬虫；  
- 爬虫Spider：对下载的内容进行解析，获得实体（目标数据）和链接进行处理；  
- 管道Item Pipeline：处理抽取出的实体，进行持久化、有效性验证等操作；  
- 下载中间件Downloader Middlewares：对下载器功能的拓展；  
- 爬虫中间件Spider Middlewares：对爬虫的拓展;  

其中，主要需要自定义的组件为Spider和Item Pipeline。  

快速构建一个Scrapy爬虫项目步骤：  

- 第一步，新建项目：`> scrapy startproject example_project`  
- 第二步，创建爬虫：  

```shell
> cd example_project
> scrapy genspider example_spider
```

- 第三步，编写爬虫、管道等组件，配置`settings.py`文件  
  - `example_spider.py`：编写`start_request()`、`parse()`等方法设置请求和解析逻辑；  
  - `items.py`、`itempipeline.py`：构建实体和编写存储逻辑；  
  - `settings.py`：配置项目的一些设置，如`user-agent`、`header`等；  

- 第四步，启动爬虫
  - 在项目目录内执行`> scrapy crawl example_spider`
  - 也可以编写脚本，通过执行脚本启动爬虫：

  ```python
  import os
  import sys
  from scrapy import cmdline
  
  base_path = os.path.dirname(os.path.abspath(__file__))
  sys.path.append(base_path)
  os.chdir(base_path)
  cmdline.execute(['scrapy', 'crawl', 'example_spider'])
  ```

## 5. 反反爬虫

在爬取猫眼电影网站时，遇到了猫眼的一些反爬虫措施限制，比如：  

- 第一次访问需要先进行验证  
- 访问次数过多可能导致IP被封  

针对上述问题，本周学习阶段可以用到的一些技巧有：  

- 先在浏览器进行验证，之后将得到的cookie设置到爬虫的header中以避开验证；（比较适合一次性爬取使用，多次爬取需要及时更换cookie）  
- 随机使用多个user-agent  
- 降低爬虫访问频率
- 设置代理池

## 6. 遇到的问题及解决

### 反爬虫

问题：如上述所说，在爬取猫眼电影网站时遇到了反爬虫；由于重定向到验证页面的原因导致解析不成功  
解决：目前比较简单粗暴的办法就是将浏览器已验证过的页面的cookie配置到爬虫的header中以避开验证（一次性手段）  

### 混合缩进问题

在编写python代码时，一定要主要统一缩进格式（或4个空格，或使用tab），混合缩进可能导致明面上看，代码格式没问题，但执行时总会提示莫名其妙的indent错误  