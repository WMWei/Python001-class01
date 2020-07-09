# Scrapy settings for maoyantop10_2 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


BOT_NAME = 'maoyantop10_2'

SPIDER_MODULES = ['maoyantop10_2.spiders']
NEWSPIDER_MODULE = 'maoyantop10_2.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'maoyantop10_2 (+http://www.yourdomain.com)'
# 设置多个UA


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
DEFAULT_REQUEST_HEADERS  = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Host': 'm.maoyan.com',
    'Sec-Fetch-Dest' : 'document',
    'Sec-Fetch-Mode' : 'navigate',
    'Sec-Fetch-Site' : 'none',
    'Sec-Fetch-User' : '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile \
        Safari/537.36',
    'Cookie':'_lxsdk_cuid=172e0eb1d59c8-0197d69755071c-4353761-e1000-\
        172e0eb1d5ac8;_lxsdk=\
        F2450FB0B54311EAAD7CEBC74F78E0F9A995E2BA961A45BEAA1E54FBA23E0D17;\
        Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1592911404,1593251456; \
        __mta=42709786.1592911404483.1593330723424.1593330927178.7; \
        uuid_n_v=v1;iuuid=\
        723B30C0C0A511EAA653931933BC0765FC64FDC5AB1E454CAB8C1EEAF82A13C5; \
        webp=true; ci=50%2C%E6%9D%AD%E5%B7%9E'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'maoyantop10_2.middlewares.Maoyantop102SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'maoyantop10_2.middlewares.Maoyantop102DownloaderMiddleware': 543,
    'maoyantop10_2.middlewares.RandomHttpProxyMiddleware': 400,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'maoyantop10_2.pipelines.Maoyantop102Pipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# MYSQL SETTING
MYSQL_HOST = '127.0.0.1'
MYSQL_POST = 3306
MYSQL_SCHEMAS = 'scrapy_demo'
MYSQL_TABLE = 'maoyantop10'
MYSQL_USER = 'scrapy'
MYSQL_PSW = '123456'
MYSQL_CHARSET='utf8mb4'
# CUSTOM SETTINGS
# PROXIES
HTTPS_PROXY_LIST = [
    'https://183.141.63.219:4236',
    'https://221.1.124.51:4284',
    'https://125.86.166.232:4237',
]
# LOG SETTINGS
import time
LOG_ENABLED=True
LOG_FILE = f"{time.strftime('%Y%m%d-%H%M%S')}.log"
LOG_ENCODING='utf-8'
LOG_FORMAT='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT='%Y-%m-%d %H:%M:%S'

