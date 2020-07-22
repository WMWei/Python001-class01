from threading import Thread, Event
from queue import Queue
# from urllib.parse import parse_qs
import time

import requests

import settings
import tools 


# 获取会话
def get_session(retry_times: int=0):
    if retry_times > settings.RETRY_TIMES:
        print(f'>>> 重新访问次数{settings.HOME_URL}超过{settings.RETRY_TIMES}次，获取cookies失败！')
        return None, None
    else:
        try:
            print(f'>>> 尝试访问{settings.HOME_URL}获得cookies')
            # 由于settings.HOME_HEADERS和settings.SEARCH_HEADERS使用了fake_useragent，这里重新赋值以确保在子线程中固定值
            home_headers = settings.HOME_HEADERS
            search_headers = settings.SEARCH_HEADERS
            session = requests.Session()
            session.get(settings.HOME_URL, headers=home_headers)
            return session, search_headers
        except Exception as e:
            print(f'>>> 尝试访问{settings.HOME_URL}获取cookies失败，将重试')
            time.sleep(settings.REQUEST_GAP)
            return get_session(retry_times + 1)


# 下载器线程
class RequestThread(Thread):
    def __init__(self,
                session: requests.Session,
                headers: dict,
                urls_queue: Queue,
                page_queue: Queue):
        super().__init__()
        self.session = session
        self.headers = headers
        self.urls_queue = urls_queue
        self.page_queue = page_queue
        print(f'>>> 创建页面请求进程<{self.name}>')

    def run(self):
        print(f'>>> 启动页面请求进程<{self.name}>')
        while not tools.check_position_count():
            if self.urls_queue.empty():
                break
            try:
                urls_info = self.urls_queue.get()
                retry_times = urls_info['retry_times']
                url = urls_info['url']
                city = urls_info['city']
                if tools.check_position_count(city):
                    continue
                self.request(url, city, retry_times)
            except Exception as e:
                print(f'''<{self.name}>: 请求页面{url}失败，将在后续进行重试！
                错误信息: {e}''')
                
                if retry_times <= settings.RETRY_TIMES:
                    self.urls_queue.put({'url': url,
                                        'city': city,
                                        'retry_times': retry_times + 1})
            finally:
                self.urls_queue.task_done()
        print(f'>>> 页面请求进程<{self.name}>结束')

    def request(self, url, city, retry_times):
        if retry_times <= settings.RETRY_TIMES:
            print(f'<{self.name}>: 开始下载{url}...')
            content = self.session.get(url=url,
                                      headers=self.headers,
                                      cookies=self.session.cookies,)
            # 适当降低频率
            time.sleep(settings.REQUEST_GAP)
            if content.json()['state'] == 1:
                print(f'<{self.name}>: 页面{url}下载完成！')
                self.page_queue.put({'page': content, 
                                    'city': city,})
            else:
                print(f'<{self.name}>: 未获取到目标页面{url}，正在更换cookies重试')
                self.change_cookie()
                self.urls_queue.put({'url': page.request.url,
                                    'city': page_info['city'],
                                    'retry_times': retry_times + 1})
        else:
            print(f'<{self.name}>: 重复请求{url}超过{settings.RETRY_TIMES}次，放弃该页面。')

    def change_cookie(self):
        session, headers = get_session()
        if session:
            self.session = session
            self.headers = headers


class ParserThread(Thread):
    def __init__(self,
                page_queue: Queue,
                data_queue: Queue,):
        super().__init__()
        self.page_queue = page_queue
        self.data_queue = data_queue
        # self.urls_queue = urls_queue
        # self._stop_event = Event()
        print(f'>>> 创建页面解析进程<{self.name}>')

    def run(self):
        print(f'>>> 启动页面解析进程<{self.name}>')
        # 当收集数据未达到目标值时，执行循环
        while not tools.check_position_count():
            try:
                page_info = self.page_queue.get()
                if tools.check_position_count(page_info['city']):
                    continue
                self.parser(page_info['page'])
            except Exception as e:
                print(f'<{self.name}>: 解析页出错：{e}')
            finally:
                self.page_queue.task_done()
        print(f'>>> 页面解析进程<{self.name}>结束')

    def parser(self, content):
        json_page = content.json()
        # 得到目标页面content.data.page
        print(f'<{self.name}>: 解析页面{content.request.url}')
        infos = json_page['content']['data']['page']['result']
        for info_tag in infos:
            position_info = {
                'position_id': info_tag['positionId'], 
                'position_name': info_tag['positionName'],
                'city': info_tag['city'],
                'created': info_tag['createTime'],
                'salary': info_tag['salary'],
                'company_id': info_tag['companyId'],
                'company': info_tag['companyName'],
                'company_full_name': info_tag['companyFullName'],
            }
            self.data_queue.put(position_info)
        # else:
        #     print(f'<{self.name}>: 未获取到目标页面，{page.request.url}解析失败，将在后续重新下载！')
        #     if retry_times <= settings.RETRY_TIMES:
        #         retry_times += 1
        #         self.urls_queue.put({'url': page.request.url,
        #                             'city': page_info['city'],
        #                             'retry_times': retry_times})
    
    # def stop(self):
    #     self._stop_event.set()

    # def stopped(self):
    #     return self._stop_event.is_set()


# if __name__ == '__main__':
#     x = settings.USER_AGENT
#     y = settings.USER_AGENT
#     print(f'{x},\n{y}')
