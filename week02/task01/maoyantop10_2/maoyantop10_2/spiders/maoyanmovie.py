import scrapy
from maoyantop10_2.items import Maoyantop102Item

class MaoyanmovieSpider(scrapy.Spider):
    name = 'maoyanmovie'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        try:
            movie_tags = response.xpath('//div[@class="movie-item-hover"]/a')[:10]
            for tag in movie_tags:
                movie_item = Maoyantop102Item()
                link = tag.xpath('@href').get()
                infos = tag.xpath('div/div[contains(@class, "movie-hover-title")]')
                movie_item['link'] = f'https://{self.allowed_domains[0]}{link}'
                movie_item['name'] = infos[0].xpath('@title').get()
                movie_item['movie_type'] = infos[1].xpath('text()').getall()[-1].strip()
                movie_item['date'] = infos[3].xpath('text()').getall()[-1].strip()
                yield movie_item
        except Exception as e:
            self.logger.error(e)

