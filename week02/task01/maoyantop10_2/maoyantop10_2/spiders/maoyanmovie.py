import scrapy
from maoyantop10_2.items import Maoyantop102Item
import json

class MaoyanmovieSpider(scrapy.Spider):
    name = 'maoyanmovie'
    allowed_domains = ['m.maoyan.com']
    start_urls = ['https://m.maoyan.com/?showType=3#movie/classic']

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse, errback=self.errback,)

    def parse(self, response):
        try:
            movie_tags = response.xpath('//div[@class="classic-movies-list"]/a')[:10]
            for tag in movie_tags:
                movie_item = Maoyantop102Item()
                link = tag.xpath('@href').get()
                infos = tag.xpath('div/div[@class="movie-info"]')
                movie_item['link'] = f'https://{self.allowed_domains[0]}{link}'
                movie_item['name'] = infos.xpath(
                    'div[@class="title line-ellipsis"]/text()'
                    ).get()
                movie_item['movie_type'] = infos.xpath(
                    'div[@class="actors line-ellipsis"]/text()'
                    ).get()
                movie_item['date'] = infos.xpath(
                    'div[@class="show-info line-ellipsis"]/text()'
                    ).get()
                yield movie_item
        except Exception as e:
            self.logger.error(e)

    # 错误处理的回调函数
    def errback(self, failure):

        request = failure.request

        res = {
            '_id': request.meta.get('_id', ''),
            'url': request.url,
            'error_type': f"{failure.type}",
            'msg': failure.getErrorMessage(),
            'traceback': failure.getBriefTraceback(),
            'status': failure.value.response.status
        }
        self.logger.error(json.dumps(res, ensure_ascii=False))

