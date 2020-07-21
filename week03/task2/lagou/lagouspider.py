from urllib.parse import unquote_plus
from multiprocessing import Queue, Lock
from concurrent.futures import ThreadPoolExecutor as threadpool
from concurrent.futures import Future, as_completed
import json
from functools import partial
import time

import requests

import settings


def scheduler(url: str,
              params: dict,
              headers: dict,
              session: requests.Session,
              ):
    try:
        print(f'''开始搜索{params["city"]}的{params["positionName"]}信息...
                  正在下载第{params["pageNo"]}页...''')
        content = session.get(url,
                              params=params,
                              headers=headers,
                              cookies=session.cookies)
        # 频率太高可能导致部分页面下载被反爬虫限制
        time.sleep(4)
        print(f'{params["city"]}{params["positionName"]}第{params["pageNo"]}页下载完成，url: {unquote_plus(content.request.url, encoding="utf-8")}')
        return content
    except Exception as e:
        print(f'下载页面{unquote_plus(content.request.url, encoding="utf-8")}出现异常')
        print(e)
        return None


def parser(future: Future):
    data = future.result()
    if data:
        try:
            res_list = data.json()['content']['data']['page']['result']
            for info_tag in res_list:
                position_info = {
                    'id': info_tag['positionId'], 
                    'Name': info_tag['positionName'],
                    'city': info_tag['city'],
                    'created': info_tag['createTime'],
                    'salary': info_tag['salary'],
                    'company_id': info_tag['companyId'],
                    'company': info_tag['companyName'],
                    'company_full_name': info_tag['companyFullName'],
                }
                #
                print(position_info)
                # self.position_queue.put(position_info)
        except Exception as e:
            print(f'{unquote_plus(data.request.url, encoding="utf-8")}解析错误')
            print(e)


def main():
    page_size = settings.PAGE_SIZE
    pages_limit = settings.PAGE_LIMIT
    cities = settings.CITIES
    search_position = settings.POSITION
    home_header = settings.HOME_HEADER
    search_header = settings.SEARCH_HEADER
    home_url = settings.HOME_URL
    search_url = settings.SEARCH_URL

    session = requests.Session()
    try:
        # 获取cookies
        session.get(url=home_url,
                    headers=home_header)
    except Exception as e:
        print(f'请求{settings.HOME_URL}页面出错')
        print(e)
    else:
        params = ({'city': c,
                  'positionName': search_position,
                  'pageNo': p,
                  'pageSize': page_size,}
                  for c in cities
                  for p in range(1, pages_limit+1))
        scheduler_part = partial(scheduler,
                                url=search_url,
                                headers=search_header,)
        print(f'---开始爬取页面---')
        with threadpool(settings.MAX_CONCURRENT) as pool:
            futures = (pool.submit(scheduler_part, params=param, session=session)
                      for param in params)
            for future in as_completed(futures):
                future.add_done_callback(parser)
        print(f'---爬取结束---')


if __name__ == '__main__':
    main()