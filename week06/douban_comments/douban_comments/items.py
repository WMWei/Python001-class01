# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanCommentsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 评论id int
    cid = scrapy.Field()
    # 豆瓣id int
    movie_id = scrapy.Field()
    # 用户名 str
    user_name = scrapy.Field()
    # 评价 int
    rate = scrapy.Field()
    # 评价时间 str
    date = scrapy.Field()
    # 评价内容 str
    comment = scrapy.Field()


class DoubanMoviesItem(scrapy.Item):
    # 豆瓣id int
    movie_id = scrapy.Field()
    # 电影名称 str
    movie_name = scrapy.Field()
    # imdb id str
    imdb_id = scrapy.Field()
    # 上映日期 str
    release_date = scrapy.Field()
    # 电影类型 str
    movie_type = scrapy.Field()
    # 电影时长 str
    runtime = scrapy.Field()
    # 国家/地区 str
    area = scrapy.Field()
    # 语言 str
    language = scrapy.Field()
    # 图片链接 str
    img_src = scrapy.Field()
    # 评分 float
    rate = scrapy.Field()
    # 评价人数 int
    rate_count = scrapy.Field()
    # 简介 str
    indent = scrapy.Field()
    # link str
    link = scrapy.Field()
