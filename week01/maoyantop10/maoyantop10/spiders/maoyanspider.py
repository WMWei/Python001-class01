import scrapy
from maoyantop10.items import Maoyantop10Item


class MaoyanspiderSpider(scrapy.Spider):

    name = 'maoyanspider'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        movie_tags = response.xpath('//div[@class="movie-item-hover"]/a')[:10]
        for tag in movie_tags:
            movie_item = Maoyantop10Item()
            link = tag.xpath('@href').get()
            infos = tag.xpath('div/div[contains(@class, "movie-hover-title")]')
            movie_item['link'] = f'https://{self.allowed_domains[0]}{link}'
            movie_item['name'] = infos[0].xpath('@title').get()
            movie_item['movie_type'] = infos[1].xpath('text()').getall()[-1].strip()
            movie_item['date'] = infos[3].xpath('text()').getall()[-1].strip()
            yield movie_item
