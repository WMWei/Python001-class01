from threading import Lock
from functools import wraps
import time

import requests

import settings


# 用于在线程中对爬取记录计数的锁
count_lock = Lock()
# 对爬取记录计数
position_count_of_cities ={city: 0 for city in settings.CITIES}

# 检查是否收集到足够目标数据
def check_position_count(city: str=None):
    global position_count_of_cities
    if city:
        res = position_count_of_cities.get(
            city,
            settings.POSITION_COUNT) >= settings.POSITION_COUNT
        return res
    res = all(v >= settings.POSITION_COUNT 
              for v in position_count_of_cities.values())
    return res


# 累计收集数据数量
def position_count(city: str):
    global position_count_of_cityes
    if city in position_count_of_cities:
        position_count_of_cities[city] += 1


# 生产url
def gen_urls():
    for city in settings.CITIES:
        for page_no in range(1, settings.MAX_PAGE+1):
            params = {
                'city': city,
                'positionName': settings.POSITION,
                'pageNo': page_no,
                'pageSize': settings.PAGE_SIZE,
            }
            full_url = (settings.SEARCH_URL + '?' +
                        '&'.join(f'{k}={v}' for k, v in params.items()))
            print(f'>>> 生成url：{full_url}')
            yield {
                'url': full_url,
                'city': city,
                'retry_times': 0
            }


# 记录运行时间
def cost_time(fn: 'function'):
    @wraps(fn)
    def func(*args, **kwargs):
        start = time.time()
        res = fn(*args, **kwargs)
        print(f'>>> 消耗时间{time.time()-start}s')
        return res
    return func