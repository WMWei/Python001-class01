import random
import time
import logging

from fake_useragent import UserAgent


# ---查询信息配置---
# 目标城市
CITIES = [
    '北京',
    '上海',
    '广州',
    '深圳',
    # '福州',
    ]
# 爬取目标职位
POSITION = 'python'
# 页面展示是数量
PAGE_SIZE = 15  # 默认值是15，试过修改该值，但是不生效
# 每个地区最大页数
MAX_PAGE = 12
# 每个城市爬取记录数量
POSITION_COUNT = 100


# ---请求配置---
# 查询URL
# SEARCH_URL = 'https://m.lagou.com/search.json?city={city}&positionName={position}&pageNo={page}&pageSize={size}'
HOME_URL = 'https://m.lagou.com/search.html'
SEARCH_URL = 'https://m.lagou.com/search.json'
HOST = 'm.lagou.com'

# 请求头配置
USER_AGENT = UserAgent(verify_ssl=False).random
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
HOME_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': USER_AGENT,
}
SEARCH_HEADERS = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Host': HOST,
    'Referer': HOME_URL,
    'User-Agent': USER_AGENT,
    'X-Requested-With': 'XMLHttpRequest',
}

# 代理
# proxies = [
#     {'https': 'https://183.141.63.219:4236',},
#     {'https': 'https://221.1.124.51:4284',},
#     {'https': 'https://125.86.166.232:4237',},
# ]
# PROXY = random.choice(proxies)

# 重试次数
RETRY_TIMES = 3
# 请求间隔
REQUEST_GAP = random.randint(2, 5)


# ---并发配置---
MAX_CONCURRENT = 4


# ---数据库配置---
# MONGODB SETTING
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DB = 'ScrapyDemo'
MONGODB_COLNAME = 'lagou'
MONGODB_USER = 'wm'
MONGODB_PSW = '123456'


# ---日志---
LOG_FILE = f'log/{time.strftime("%Y%m%d-%H%M%S")}.log'
LOG_FORMAT = '[%(asctime)s-%(levelname)s]: %(message)s'
LOG_DATE_FORMAT = '%m/%d/%Y %H:%M:%S %p'
LOG_LEVEL = logging.INFO