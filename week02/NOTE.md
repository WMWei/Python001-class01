# Week02学习笔记

## 1 week02笔记

本周学习内容：

- 异常处理
- mySQL数据库连接与数据存储
- 反反爬虫：
  - 模拟请求头
  - POST请求和cookies验证
  - Selenium模拟浏览器行为
  - tesserct-ocr图片验证码识别
  - 代理IP和Scrapy爬虫中间件
- 分布式爬虫

## 2 第一次社群分享笔记

> Scrapy使用经验分享

### 2.1 Scrapy常用命令

- [官方Scrapy命令参考文档](https://docs.scrapy.org/en/latest/topics/commands.html#available-tool-commands)
- 查看Scrapy帮助：`> scrapy [command] --help`  
- Scrapy命令目前有14个，分两类：  
  - 全局命令：不依赖Scrapy项目执行的命令。在项目目录里运行会默认使用项目设置，否则使用默认设置；  
  - 项目命令：依赖于项目的命令，必须在项目目录中使用。Scrapy在启动时会将项目目录作为包导入，未在项目目录中使用项目命令会导致ImportError；  
![Scrapy命令分类](/week02/picture/Scrapy命令区分.jpg)

#### 常规命令：基本必用

- `startproject`：用于创建Scrapy项目
  - `scrapy startproject <projectname> [dirname]`
- `genspider`：用于创建爬虫
  - 创建爬虫：`scrapy genspider [-t template]<spidername> <domain>`
  - 查看模板：`scrapy genspider -l | --list`
- `crawl`：用于启动爬虫
  - 常规启动：`scrapy crawl <spiders>`
  - 参数：
    - `-a XX=XX`：用于初始化
    - `-s XX=XX`：用于爬取时进行设置

#### 常用命令：debug常用

- `runspider`：没有创建项目的情况下，单独运行spider
  - 运行命令：`scrapy runspider <spidername.py>`
  - 参数：
    - `--output=FILE`|`-o FILE`：将抓取结果保存到文件FILE
- `shell`：模拟Scrapy流程，在不启动spider的情况下调试代码
  - `scrapy shell [url | html_file]`
- `check`：检查语法错误
  - `scrapy check [-l] <spidername>`
- `list`：列出所有spider
  - `scrapy list`
- `parse`：测试某个parse方法
  - `scrapy parse <url> [option]`
  - 参数：
    - `-c | --callback`可以指定parse方法，默认使用parse

#### 不常用命令

- `settings`：`scarpy settings --get=XXX`，获取settings.py文档相应配置参数
- `fetch`：`scrapy fetch <url>`，向url发起请求，输出到stdout
- `view`：`scrapy view <url>`，向url发起请求，将获取的相应使用浏览器打开
- `version`：`scrapy version [-v]`，查看scrapy版本，`-v`获取相应依赖包版本
- `edit`：`scrapy edit <spidername>`，使用编辑器打开spider，依赖于`EDITOR`设置
- `bench`：`scrapy bench`，基准测试，生成本地HTTP服务器并以最大可能的速度爬取，用于测试Scrapy在本地PC的性能

### 2.2 Scrapy爬虫经验分享

1. 不建议直接从开发者工具中复制xpath路径
2. 在测试xpath或者css选择器时，一定要检查网页源码和开发者工具中的Elements页面是否一致（Elements页面是经过浏览器渲染的，而我们直接爬取的是源码）

### 2.3 其他tips

- Scrapy新手练习网站：Scrapy文档使用的爬取网站，[http://toscrape.com/](http://toscrape.com/)，提供虚拟数据供新手练习；  
- 启动Scrapy的两种方式：
  - 在项目目录下进行命令行启动`scrapy crawl <spider>`
  - API启动
- Scrapy启动没有任何反应：
  - 只要scrapy项目正常启动，则说明有语法错误
  - 检查是否设置了输出到日志
  - 默认等待时长`DOWNLOAD_TIMEOUT`之中没有反应，可能服务器响应慢，超时
  - 大概率被反爬
- `itempipeline`里文件保存位置：相对路径是相对于启动scrapy时的目录
- 使用scrapy自带日志功能：`scrapy.Scrapy`类自带`logger`方法，因此可以通过spider对象调用`.logger`方法使用日志，用法类似标准库[`logging`](https://docs.python.org/zh-cn/3/library/logging.html)
- 日志输出：
  - 默认输出`stdout`
  - 设置日志输出文件：  
    - `scrapy crawl <spider> --logfile xxx.log`
    - settings.py中设置`LOGFILE`
    - 在爬虫类中，使用`custom_settings`字典针对具体爬虫文件进行个性化设置（键名对应settigs.py里的相应参数）
- scrapy的response对象自带Selector对象的功能，可以直接使用`.xpath`、`.css`、`.re`
- scrapy的Selector在底层是对`parsel`库的封装，若只是要使用Selector的功能，可以直接安装第三方库`parsel`使用`parsel.Selector`即可
- scrapy也带有csv导出器[`CsvItemExporter`](https://docs.scrapy.org/en/latest/topics/exporters.html)
