from threading import Thread, Event
from queue import Queue, PriorityQueue
from urllib.parse import unquote_plus
import time

import requests

import settings
import tools 


# --------生产url--------
class ShedulerThread(Thread):
    def __init__(self, 
                urls_queue: Queue):
        super().__init__()
        self.urls_queue = urls_queue
        self.urls_info = self.gen_urls()
        print(f'>>> 创建生产url线程<{self.name}>')
    
    def run(self):
        tools.lock_print(f'>>> 启动生产url线程<{self.name}>')
        for urls_info in self.urls_info:
            if tools.check_db_position_count():
                break
            try:
                self.urls_queue.put(urls_info)
            except Exception as e:
                tools.lock_print(
                    f'<{self.name}>:'
                    f'\n- <error>: 生产url出错，将退出生产线程'
                    f'\n- <error>: {e}')
                break
        tools.lock_print(f'>>> 生产url线程线程<{self.name}>结束')

    def gen_urls(self):
        page_no = 11
        while page_no <= settings.MAX_PAGE:
            for city in settings.CITIES:
                params = {
                    'city': city,
                    'positionName': settings.POSITION,
                    'pageNo': page_no,
                    'pageSize': settings.PAGE_SIZE,
                }
                full_url = (settings.SEARCH_URL + '?' +
                            '&'.join(f'{k}={v}' for k, v in params.items()))
                tools.lock_print(f'<{self.name}>:\n- 生成url：{full_url}')
                yield {'url': full_url,
                           'city': city,
                           'retry_times': 0}
            page_no += 1


# --------下载器线程--------
class RequestThread(Thread):
    def __init__(self,
                # session: requests.Session,
                # headers: dict,
                urls_queue: Queue,
                page_queue: Queue):
        super().__init__()
        self.session = None
        self.headers = None
        self.urls_queue = urls_queue
        self.page_queue = page_queue
        print(f'>>> 创建页面请求线程<{self.name}>')

    def run(self):
        tools.lock_print(f'>>> 启动页面请求线程<{self.name}>')
        # 获取会话并判断是否成功
        if not self.get_session():
            tools.lock_print(f'<{self.name}>:\n- 获取会话失败，将退出线程')
        else:
            while True:
                try:
                    urls_info = self.urls_queue.get()
                    # 有可能存在所有页面数据不够需求数量
                    if urls_info is None:
                        break
                    retry_times = urls_info['retry_times']
                    url = urls_info['url']
                    city = urls_info['city']
                    break_flag = self.request(url, city, retry_times)
                    # 全部收集完成，则退出
                    if break_flag == 1:
                        break
                    # 相应城市收集完，则跳过
                    if break_flag == 2:
                        continue
                except Exception as e:
                    tools.lock_print(
                        f'<{self.name}>:'
                        f'\n- <error>: 请求页面{url}失败，后续将重试'
                        f'\n- <error>: {e}')
                    if retry_times <= settings.RETRY_TIMES:
                        self.urls_queue.put({
                            'url': url,
                            'city': city,
                            'retry_times': retry_times + 1})
                finally:
                    self.urls_queue.task_done()
        # 最终关闭会话
        self.session.close()
        tools.lock_print(f'>>> 页面请求线程<{self.name}>结束')

    def request(self, url: str, city: str, retry_times: int):
        if tools.check_db_position_count():
            return 1
        if tools.check_db_position_count(city):
            return 2
        if retry_times <= settings.RETRY_TIMES:
            tools.lock_print(f'<{self.name}>: \n- 开始下载{url}...')
            content = self.session.get(
                url=url,
                headers=self.headers,
                cookies=self.session.cookies,)
            # 适当降低频率
            time.sleep(settings.REQUEST_GAP)
            if content.json()['state'] == 1:
                tools.lock_print(f'<{self.name}>: \n- 页面{url}下载完成！')
                self.page_queue.put(content)
            else:
                tools.lock_print(
                    f'<{self.name}>: '
                    f'\n- 未获取到目标页面{url}，正在更换cookies重试')
                self.change_cookie()
                self.urls_queue.put((0, {
                    'url': unquote_plus(content.request.url),
                    'city': city,
                    'retry_times': retry_times + 1}))
        else:
            tools.lock_print(
                f'<{self.name}>:'
                f'\n- <error>: 重复请求{url}超过{settings.RETRY_TIMES}次，'
                f'放弃该页面')
        return 0

    def change_cookie(self):
        old_session = self.session
        # 如果获取成功
        if self.get_session():
            # 关闭当前会话
            old_session.close()

    # 获取会话
    def get_session(self, retry_times: int=0):
        if retry_times > settings.RETRY_TIMES:
            tools.lock_print(
                f'<{self.name}>: \n- <error>: '
                f'访问次数{settings.HOME_URL}超过{settings.RETRY_TIMES}次，'
                f'获取cookies失败！')
            return False
        else:
            try:
                tools.lock_print(f'>>> 尝试访问{settings.HOME_URL}获得cookies')
                # 由于settings.HOME_HEADERS和settings.SEARCH_HEADERS使用了fake_useragent，这里重新赋值以确保在子线程中固定值
                home_headers = settings.HOME_HEADERS
                self.headers = settings.SEARCH_HEADERS
                self.session = requests.Session()
                self.session.get(settings.HOME_URL, headers=home_headers)
                return True
            except Exception as e:
                tools.lock_print(
                    f'>>> <error>: '
                    f'尝试访问{settings.HOME_URL}获取cookies失败，将重试'
                    f'\n- 错误信息: {e}')
                time.sleep(settings.REQUEST_GAP)
                return self.get_session(retry_times + 1)

class ParserThread(Thread):
    def __init__(self,
                page_queue: Queue,
                data_queue: Queue,):
        super().__init__()
        self.page_queue = page_queue
        self.data_queue = data_queue

        print(f'>>> 创建页面解析线程<{self.name}>')

    def run(self):
        tools.lock_print(f'>>> 启动页面解析线程<{self.name}>')
        # 当收集数据未达到目标值时，执行循环
        while True:
            try:
                page_info = self.page_queue.get()
                # 有可能存在所有页面数据不够需求数量
                if page_info is None:
                    break
                break_flag = self.parser(page_info)
                # 全部收集完成，则退出
                if break_flag == 1:
                    break
                # 当前城市收集完成，则跳过
                if break_flag == 2:
                    continue
            except Exception as e:
                tools.lock_print(f'<{self.name}>: \n- 解析页面出错: {e}')
            finally:
                self.page_queue.task_done()
        tools.lock_print(f'>>> 页面解析线程<{self.name}>结束')

    def parser(self, content):
        if tools.check_db_position_count():
            return 1
        json_page = content.json()

        city = json_page['content']['data']['custom']['city']
        if tools.check_db_position_count(city):
            return 2
        
        tools.lock_print(f'<{self.name}>: \n- 解析页面{unquote_plus(content.request.url)}')
        infos = json_page['content']['data']['page']['result']

        for info_tag in infos:
            position_info = {
                'position_name': info_tag['positionName'],
                'city': info_tag['city'],
                'salary': info_tag['salary'],
            }
        
            self.data_queue.put(position_info)
        return 0
