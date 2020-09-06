from datetime import datetime, timedelta, timezone
import re

import scrapy
from scrapy.http.request import Request
from snownlp import SnowNLP

from smzdm.items import ProductItem, CommentItem


class SmzdmCommentsSpider(scrapy.Spider):
    name = 'smzdm_comments'
    allowed_domains = ['www.smzdm.com']
    start_urls = ['http://www.smzdm.com/fenlei']

    def start_requests(self):
        for i in self.start_urls:
            yield Request(url=i, callback=self.tag_parse)

    def tag_parse(self, response):
        # 获取前十个分类
        tag_urls = response.xpath(
            '//div[@class="title"]/h2/a/@href'
        ).getall()[:10]
        for link in tag_urls:
            category_en = link.split('/')[-2]
            # 24小时排行
            yield Request(
                url=link + 'h5c4s0f0t0p1/', 
                meta={'category_en': category_en},
                callback=self.index_parse)

    # 获得商品页和评论页
    def index_parse(self, response):
        category_en = response.meta['category_en']
        products_info = response.xpath(
            '//div[@class="feed-block z-hor-feed"]'
        )[:10]

        for product in products_info:
            item = ProductItem()
            # 链接
            product_link = product.xpath(
                'div[@class="z-feed-content "]'
                '/h5/a/@href'
            ).get().strip()
            # pid
            pid = product_link.split('/')[-2]
            item['link'] = product_link
            item['pid'] = pid
            # 产品名称
            item['title'] = product.xpath(
                'div[@class="z-feed-content "]'
                '/h5/a/text()'
            ).get().strip()
            # 价格
            item['price'] = product.xpath(
                'div[@class="z-feed-content "]'
                '/div[@class="z-highlight"]'
            ).xpath('string(.)').get().strip()
            # 出处
            item['price_from'] = product.xpath(
                'div[@class="z-feed-content "]'
                '/div[@class="z-feed-foot"]'
                '/div[@class="z-feed-foot-r"]'
                '/span/a/text()'
            ).get().strip()
            # 分类
            item['category'] = response.xpath(
                '//h1[@class="category-title"]/text()'
            ).get().strip()
            item['category_en'] = category_en
            # 图片
            item['img'] = product.xpath(
                'div[@class="z-feed-img"]'
                '/a/img/@src'
            ).get().strip()
            # 时间
            pub_date_str = product.xpath(\
                'div[@class="z-feed-content "]'
                '/div[@class="z-feed-foot"]'
                '/div[@class="z-feed-foot-r"]'
                '/span/text()'
            ).get().strip()
            item['pub_date'] = self.get_datetime(pub_date_str)
            print(item['pub_date'])
            yield item

            yield Request(
                url=product_link,
                meta={'pid': pid},
                callback=self.comment_parse,
            )

    # 商品内容解析
    def comment_parse(self, response):
        # 处理评论信息
        pid = response.meta['pid']
        comment_items = response.xpath(
            '//div[@id="commentTabBlockNew"]'
            '//li[@class="comment_list"]'
        )
        for comment in comment_items:
            comment_item = CommentItem()
            comment_item['pid'] = pid
            comment_item['cid'] = comment.xpath(
                'div[@class="comment_conBox"]'
                '/div[@class="comment_conWrap"]'
                '//input/@comment-id'
            ).get().strip()
            comment_item['uid'] = comment.xpath(
                'div[@class="comment_conBox"]'
                '/div[@class="comment_avatar_time "]'
                '/a/@usmzdmid'
            ).get().strip()
            comment_item['username'] = comment.xpath(
                'div[@class="comment_conBox"]'
                '/div[@class="comment_avatar_time "]'
                '/a/span/text()'
            ).get().strip()
            comment_item['comment'] = comment.xpath(
                'div[@class="comment_conBox"]'
                '/div[@class="comment_conWrap"]'
                '/div[@class="comment_con"]'
                '/p/span'
            ).xpath('string(.)').get().strip()
            datetime_str = comment.xpath(
                'div[@class="comment_conBox"]'
                '/div[@class="comment_avatar_time "]'
                '/div[@class="time"]/text()'
            ).get().strip()
            comment_item['pub_date'] = self.get_datetime(datetime_str)
            comment_item['avatar'] = comment.xpath(
                'div[@class="comment_avatar"]'
                '//a[@class="user-avatar"]/img/@src'
            ).get().strip()
            # 回复评论
            parent_comment = comment.xpath(
                'div[@class="comment_conBox"]'
                '/div[@class="blockquote_wrap"]'
                '/blockquote/@blockquote_cid'
            ).getall()
            
            if parent_comment:
                comment_item['parent_cid'] = parent_comment[-1].strip()
            else:
                comment_item['parent_cid'] = None
            # 情感分析
            comment_item['sentiments'] = SnowNLP(
                comment_item['comment']
            ).sentiments
            yield comment_item

        # 翻页
        pagedown_url = response.xpath(
            '//li[@class="pagedown"]/a/@href'
        ).getall()

        if pagedown_url:
            yield Request(
                url=pagedown_url[0],
                meta={'pid': pid},
                callback=self.comment_parse,
            )

    @staticmethod
    def get_datetime(datetime_str: str) -> datetime:
        # 提供的发布时间不完整，需要处理
        tz = timezone(offset=timedelta(hours=8))
        now = datetime.now(tz)

        regexp = re.compile('(\d+?)(\D+?)前')
        datetime_match = regexp.search(datetime_str)
        # xx小时前
        if datetime_match:
            if datetime_match.group(2) == '小时':
                return now - timedelta(hours=int(datetime_match.group(1)))
            if datetime_match.group(2) == '分钟':
                return now - timedelta(minutes=int(datetime_match.group(1)))
            if datetime_match.group(2) == '秒':
                return now - timedelta(seconds=int(datetime_match.group(1)))
        # xx-xx xx:xx
        elif len(datetime_str) == 11:
            return datetime.strptime(
                       datetime_str,
                       '%m-%d %H:%M',
                   ).replace(
                       year=now.year,
                       tzinfo=tz
                   )
        # xx-xx-xx xx:xx
        elif len(datetime_str) == 13:
            return datetime.strptime(
                       datetime_str,
                       '%Y-%m-%d %H:%M',
                   ).replace(tzinfo=tz)
        else:
            return None