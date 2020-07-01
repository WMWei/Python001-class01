'''
安装并使用 requests、bs4 库，爬取猫眼电影的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
'''

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import os.path


class MaoyanMovie(object):
    def __init__(self, host, start_url, header, limit=10):
        self.host = host
        self.header = header
        self.start_url = start_url
        self.content = self.get_html(self.start_url, self.header)
        self.movies = self.get_movies(self.content)

    def get_html(self, url, header):
        return requests.get(url, headers=header).text

    # 解析页面
    def get_movies(self, page, limit=10):
        bs_page = bs(page, 'html.parser')
        count = 0
        for movie_item in bs_page.find_all('div', attrs={'class': 'film-channel'}):
            if count < limit:
                movie = {}
                movie['url'] = self.host + movie_item.find('a').get('href')
                movie_info = movie_item.find_all(
                    'div', 
                    attrs={'class': 'movie-hover-title'})
                movie['title'] = movie_info[0].get('title')
                movie['type'] = movie_info[1].span.next_sibling.strip()
                movie['date'] = movie_info[3].span.next_sibling.strip()
                yield movie
                count += 1

    # 保存
    def save(self, path):
        movie_df = pd.DataFrame(data=self.movies)
        if os.path.splitext(path)[-1] == '.csv':
            movie_df.to_csv(path, encoding='utf-8', index=False,)
        else:
            print(movie_df)


if __name__ == '__main__':
    # 手动设置cookies来避开页面验证
    # 一次性的反反爬虫手段，多次使用需要手动修改cookie
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'maoyan.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Cookie': 'uuid_n_v=v1; \
            uuid=C8BDDBE0B54811EA8B56A5EC695B0A7354D618B929A648608C072AD80506CCB7; \
            mojo-uuid=8ad3f3958fb485f16ba407b0d546f84b; \
            _lxsdk_cuid=172e10acba162-0cde9cd230ad27-4c302372-e1000-172e10acba2c8; \
            _lxsdk=C8BDDBE0B54811EA8B56A5EC695B0A7354D618B929A648608C072AD80506CCB7;\
             Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1592913482,1593259977,\
            1593330056,1593600565; __mta=142573197.1592913482295.1593330828227.\
            1593600567075.8; \
            _csrf=1fdb10ad459e11ad235a622923b30afc3e86291f0cc854ac66f413388c357139; \
            mojo-trace-id=1; mojo-session-id=\
            {"id":"d8f1475355b34acba5b36902ac250b97","time":1593600563778}; \
            Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593600565; \
            _lxsdk_s=17309fee384-b8-4c0-1de%7C%7C2'
    }
    host = 'https://maoyan.com'
    url = '{}/films?showType=3'.format(host)
    csv_path = './week01/maoyanmovie_bs/maoyantop10.csv'
    maoyan_movie = MaoyanMovie(host=host, start_url=url, header=header,)
    maoyan_movie.save(csv_path)

