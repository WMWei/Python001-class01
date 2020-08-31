# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    # 优惠名称
    title = scrapy.Field()
    # 产品价格
    price = scrapy.Field()
    # 发布时间
    pub_date = scrapy.Field()
    # 产品来源
    price_from = scrapy.Field()
    # 产品类别
    category = scrapy.Field()
    category_en = scrapy.Field()
    # id
    pid = scrapy.Field()
    # img
    img = scrapy.Field()
    # link
    link = scrapy.Field()


class CommentItem(scrapy.Item):
    # 评论id
    cid = scrapy.Field()
    # 用户id
    uid = scrapy.Field()
    # 用户名称
    username = scrapy.Field()
    # 评论
    comment = scrapy.Field()
    # 发布时间
    pub_date = scrapy.Field()
    # 头像
    avatar = scrapy.Field()
    # 回复评论
    parent_cid = scrapy.Field()
    # 商品id
    pid = scrapy.Field()
    # 情感
    sentiments = scrapy.Field()