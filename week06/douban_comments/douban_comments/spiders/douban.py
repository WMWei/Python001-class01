import re
from datetime import datetime

import scrapy

from douban_comments.items import DoubanCommentsItem, DoubanMoviesItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    # def parse(self, response):
    #     pass

    def start_requests(self):
        url = 'https://movie.douban.com/top250?start={}&filter='
        urls = (url.format(i * 25) for i in range(1))
        for link in urls:
            yield scrapy.Request(url=link, callback=self.list_parse)
    
    def list_parse(self, response):
        links = response.xpath('//div[@class="hd"]/a/@href').getall()
        for link in links:
            item = DoubanMoviesItem()
            item['link'] = link
            item['douban_id'] = int(link.strip('/').split('/')[-1])
            yield scrapy.Request(url=link, 
                                 meta={'item': item}, 
                                 callback=self.item_parse)
    
    def item_parse(self, response):
        movie_item = response.meta['item']
        # 电影名称 str
        movie_item['name'] = response.xpath(
            '//span[@property="v:itemreviewed"]'
            '/text()'
        ).get()
        # imdb id str
        movie_item['imdb_id'] = response.xpath(
            '//div[@id="info"]/a[last()]/text()'
        ).get()
        # 上映日期 str
        movie_item['release_date'] = response.xpath(
            '//span[@property="v:initialReleaseDate"]/text()'
        ).get()
        # 电影类型 str
        movie_item['movie_type'] = '/'.join(response.xpath(
            '//span[@property="v:genre"]/text()'
        ).getall())
        # 电影时长 str
        movie_item['runtime'] = response.xpath(
            '//span[@property="v:runtime"]/text()'
        ).get()
        # 国家/地区 str
        movie_item['area'] = response.xpath(
            '//div[@id="info"]/span[text()="制片国家/地区:"]'
            '/following-sibling::text()'
        ).get().replace(' ', '')
        # 语言 str
        movie_item['language'] = response.xpath(
            '//div[@id="info"]/span[text()="语言:"]'
            '/following-sibling::text()'
        ).get().replace(' ', '')
        # 图片链接 str 
        movie_item['img_src'] = response.xpath(
            '//a[@class="nbgnbg"]/img/@src'
        ).get()
        # 评分 float
        movie_item['rate'] = float(response.xpath(
            '//strong[@property="v:average"]/text()'
        ).get())
        # 评价人数 int
        movie_item['rate_count'] = int(response.xpath(
            '//span[@property="v:votes"]/text()'
        ).get())
        # 简介 str
        movie_item['indent'] = re.sub(
            '\s+',
            '\n',
            ''.join(response.xpath(
                '//span[@property="v:summary"]/text()'
            ).getall())
        ).strip()
        yield movie_item

        comments_link = (movie_item['link'] + 
                        'comments?start={}&sort=new_score&status=P')
        item = DoubanCommentsItem()
        item['douban_id'] = movie_item['douban_id']
        # 只取十页
        comments_links = (comments_link.format(i * 20) for i in range(1))
        for link in comments_links:
            yield scrapy.Request(url=link,
                                 meta={'item': item},
                                 callback=self.comments_parse)
        

    def comments_parse(self, response):
        comments_item = response.meta['item']
        # 评分与评价映射
        RATING_MAP = {
            '力荐': 5,
            '推荐': 4,
            '还行': 3,
            '较差': 2,
            '很差': 1,
        }
        comments_infos = response.xpath('//div[@class="comment-item"]')
        for comment in comments_infos:
            # 评论id int
            comments_item['cid'] = comment.xpath('@data-cid').get()
            # 用户名 str
            comments_item['user_name'] = comment.xpath(
                'div[@class="comment"]/h3'
                '/span[@class="comment-info"]/a/text()'
            ).get().strip()
            # //span[@class="comment-info"]/a/text()
            # 评价 str
            comments_item['rate'] = RATING_MAP.get(comment.xpath(
                'div[@class="comment"]/h3'
                '/span[@class="comment-info"]'
                '/span[contains(@class, "rating")]/@title'
            ).get())
            # 评价时间 str
            date_str = comment.xpath(
                'div[@class="comment"]/h3'
                '/span[@class="comment-info"]'
                '/span[@class="comment-time "]/@title'
            ).get()
            comments_item['date'] = datetime.strptime(
                date_str,
                '%Y-%m-%d %H:%M:%S'
            )
            # 评价内容 str
            comments_item['comment'] = re.sub(
                '\s+',
                '\n',
                comment.xpath(
                'div[@class="comment"]/p/span/text()'
                ).get()
            ).strip()
            yield comments_item