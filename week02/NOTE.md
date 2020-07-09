# Week02学习笔记

## 1 week02知识点

### 1.1 异常处理

- 一般异常处理：
  - `try ... except ... finally`语句捕获和处理异常
  - `raise`抛出异常
  - 自定义异常类总是继承自`Exception`类及其子类
- Scrapy的异常处理：
  - 一样可以通过`try ... except ... finally`捕获
  - 可以使用`scrapy.logger.error()`将捕获的异常信息记录到日志
  - 对下载器，可以通过`errback`参数调用异常回调函数来处理异常

### 1.2 MySQL数据库连接

- 使用模块`pymysql`
- 步骤：
  1. 创建数据库连接：`pymysql.connect(host=hostport=port,user=user,password=psw,db=db,charset=charset,)`
  2. 创建游标：`conn.cursor()`，需要利用游标操作数据库
  3. 执行SQL：`cur.excute(sql, args)`
  4. 提交事务：`cur.commit()`
  5. 关闭事务：`cur.close()`

- 在Scrapy中，通过在`pipelines.py`中使用`pymysql`库来将爬取数据存储到数据库
  - 利用`open_spider()`、`from_crawler()`、`__init__()`处理数据库连接、初始化等问题
  - 利用`process_item()`进行数据存储
  - 利用`close_spider()`处理事务提交、数据库关闭等收尾工作
  - 另外，可以利用`spider.settings.get()`获取`settings.py`中的配置信息

### 1.3 反反爬虫

#### 模拟请求头

利用`fake_useragent.USERAGENT()`模块可以方便的使用随机`USER-AGENT`

#### 使用cookie模拟登陆

- cookie可以维持用户跟服务器的会话状态，经常用于用户登录、身份验证等场景
- 利用`requests.session()`创建会话之后再进行请求，可以
  - 重用tcp连接，提高爬虫运行效率
  - 通过session使用cookie
- 模拟登陆过程：
  1. 创建会话
  2. 发出POST请求
  3. 获取cookie，利用cookie请求其他登陆后才可获取的页面

#### 使用WebDriver模拟浏览器行为

- 许多页面会使用AJAX技术来加载和渲染，通过`requsets`直接爬取页面，获不到渲染之后的源码
- 想要获得渲染后的页面源码，两个方法:
  - 方法一：通过开发者工具分析AJAX请求，找到实际加载目标数据的请求；通过对该URL发出请求得到目标数据；
  - 方法二：利用WebDriver模拟浏览器行为
    - 需要工具：
      - `selenium`模块
      - 相应浏览器驱动，如Chrome对应的`chromedriver`驱动（需要与浏览器版本匹配）
    - 步骤：
      1. 利用`WebDriver`构造driver对象（相当于构造一个浏览器）
      2. 通过driver对象访问页面，操作元素
    - 注意点：由于AJAX是异步加载，在请求成功后页面可能还未完全加载完成。为了保证能正确获取目标元素，应该设置等待时间来保证页面加载完全：
      - 方式一：通过`sleep(30)`设置等待
      - 方式二：利用`driver.implicitly_wait(30)`设置隐式等待，模块会在遇到要加载的页面时进行等待
      - 方式三：利用`WebDriverWait()`进行精确的等待设置，如

      ```python
      WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[@class='form-wrapper']"
                )))
      ```

#### 图形验证码识别

- 使用模块：`pytesseract`、`Pillow`
- 处理流程：
  1. 利用`requests`等http库下载验证码图片
  2. 利用`Pillow`库对图片进行灰度、二值化等处理使得验证码文字部分更加明显
  3. 利用`pytesseract`库进行识别

### 1.4 Scrapy下载中间件与代理

- 场景：由于网站的反爬虫措施，发起的大量并发请求的同一个IP将被列为风险IP而被封禁，导致爬虫失效
- 为了避免IP被封禁，可以使用多个IP对目标网站进行访问
- Scrapy提供下载中间件（DownloadMiddlewares）来处理下载器（Downloader）执行前和执行后的一些操作，其中就包括设置代理IP

#### Scrapy使用系统代理

1. 设置系统代理，如linux下使用`export http://xxx.xxx.xxx.xxx:xxxx`设置系统代理
2. `settings.py`中启用标准下载中间件的代理中间件（`scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware`）来设置代理

#### Scrapy自定义代理中间件

- 项目目录下的`middlewares.py`文件用于自定义各种中间件，包括爬虫中间件、下载中间件、代理中间件
- 通过继承`HttpProxyMiddleware`中间件，并重写相应的方法，可以自定义代理的设置：
  1. `settings.py`中启用自定义代理中间件，并配置相应代理列表
  2. `middlewares.py`中自定义代理中间件类，继承自`HttpProxyMiddleware`类，并根据需要重写相应方法
    - `from_crawler()`，`__init__()`构造代理中间件
    - `_get_proxy()`获取代理
    - `_set_proxy()`，`process_proxy()`设置代理
- 注意点：只有代理的协议和目标网站可接受协议匹配时，代理才会生效；如网站只使用https协议，那么使用http协议的代理，`process_proxy()`并不会令其生效

### 1.5 分布式爬虫

爬取一些大型网站时，可能因为CPU计算能力不够、或者单机网络带宽不够、或者内存不够等原因，需要多台电脑配合，让Scrapy进行多机通信。

Scrapy原生不支持分布式爬虫，需要Redis实现队列和管道共享。`scrapy-redis`包提供了Scrapy和Redis的集成：

- 将Scrapy的`Spider`类替换成`RedisSpider`
- 使用redis实现调度器的队列
- 使用redis实现item pipeline

具体实现：

- 依然使用Scrapy建立和编写项目
- 在`settings.py`配置替换的组件

  ```shell
  # Scheduler的QUEUE
  SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
  # 去重
  DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
  # Requests的默认优先级队列
  SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
  # 将Requests队列持久化到Redis，可支持暂停或重启爬虫
  SCHEDULER_PERSIST = True
  # 将爬取到的items保存到Redis
  ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
  }
  ```

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
