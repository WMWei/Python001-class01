'''
安装并使用 requests、bs4 库，爬取猫眼电影的前 10 个电影名称、电影类型和上映时间，并以 UTF-8 字符集保存到 csv 格式的文件中。
'''

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


# 获取页面
def get_page(url, headers):
    return requests.get(url, headers=headers).text


# 获取目录页的各个电影链接
def get_movie_url(page, limit=10):
    bs_page = bs(page, 'html.parser')
    count = 0
    for movie_item in bs_page.find_all('div', attrs={'class': 'film-channel'}):
        if count < limit:
            yield movie_item.find('a').get('href')
            count += 1


# 获取详情页中的目标信息
def get_movie_info(page):
    bs_page = bs(page, 'html.parser')
    movie_tag = bs_page.find('div', attrs={'class': 'movie-brief-container'})
    name = movie_tag.find('h1').text
    infos = movie_tag.find('ul').find_all('li')
    date = infos[2].text[:10]
    movie_type = infos[0].get_text().strip().replace(' \n ', '/')
    return name, date, movie_type


if __name__ == '__main__':
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Host': 'maoyan.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
    }
    home_url = 'https://maoyan.com{}'
    list_url = home_url.format('/films?showType=3')
    movie_infos = []
    
    list_page = get_page(list_url, header)
    movie_urls = get_movie_url(list_page)
    for url in movie_urls:
        movie_page = get_page(home_url.format(url), header)
        movie_info = get_movie_info(movie_page)
        movie_infos.append(movie_info)
    
    movies = pd.DataFrame(data=movie_infos)
    movies.to_csv('./week01/maoyantop10.csv', encoding='utf-8', index=False, header=False)
