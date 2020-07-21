# 查询信息配置
# 目标城市
CITIES = [
    '北京',
    '上海',
    '广州',
    '深圳',
    ]
# 单页面显示数量
PAGE_SIZE = 25
# 爬取页面数量
PAGE_LIMIT = 4
# 爬取目标职位
POSITION = 'python工程师'
# 查询URL
# SEARCH_URL = 'https://m.lagou.com/search.json?city={city}&positionName={position}&pageNo={page}&pageSize={size}'
HOME_URL = 'https://m.lagou.com/search.html'
SEARCH_URL = 'https://m.lagou.com/search.json'
HOST = 'm.lagou.com'

# 请求头配置
from fake_useragent import UserAgent

# USER_AGENT = UserAgent().random
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
HOME_HEADER = {
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
SEARCH_HEADER = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Host': HOST,
    'Referer': HOME_URL,
    'User-Agent': USER_AGENT,
    'X-Requested-With': 'XMLHttpRequest',
}

# 并发配置
MAX_CONCURRENT = 4

# 数据库配置