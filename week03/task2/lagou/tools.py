from threading import Lock
from functools import wraps
from collections import Counter
import time

import requests
# import pandas as pd

import settings


# ---------计数和处理重复---------
# 对数据库入库数据计数
db_position_count = Counter({city: 0 for city in settings.CITIES})

# 检查入库数量是否满足
def check_db_position_count(city: str=None) -> bool:
    if city:
        return db_position_count[city] >= settings.POSITION_COUNT
    return all(db_position_count[city] >= settings.POSITION_COUNT 
              for city in settings.CITIES)


# ---------锁---------
# 用于打印
print_lock = Lock()
# 用于在线程中对爬取记录计数的锁
db_count_lock = Lock()
parser_count_lock = Lock()


# 用于在线程中打印
def lock_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)


# ---------记录运行时间---------
def cost_time(fn: 'function'):
    @wraps(fn)
    def func(*args, **kwargs):
        start = time.time()
        res = fn(*args, **kwargs)
        print(f'>>> 消耗时间{time.time()-start}s')
        return res
    return func