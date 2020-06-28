import scrapy
from maoyantop10.items import Maoyantop10Item


class MaoyanspiderSpider(scrapy.Spider):
    name = 'maoyanspider'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']


    def start_requests(self):
        for link in self.start_urls:
            yield scrapy.Request(url=link, callback=self.home_parse)

    def home_parse(self, response):
        movie_urls = response.xpath('//div[@class="movie-item film-channel"]/a/@href').getall()[:10]
        for link in movie_urls:
            movie_item = Maoyantop10Item()
            url = f'https://{self.allowed_domains[0]}{link}'
            # movie_item['link'] = url
            yield scrapy.Request(url=url, meta={'item': movie_item}, callback=self.info_parse)

    def info_parse(self, response):
        movie_item = response.meta['item']
        movie_tag = response.xpath('//div[@class="movie-brief-container"]')[0]
        movie_name = movie_tag.xpath('./h1/text()').get()
        movie_date = movie_tag.xpath('./ul/li[3]/text()').get()[:10]
        movie_type = '/'.join(movie_tag.xpath('./ul/li[1]/a/text()').getall()).replace(' ', '')
        movie_item['name'] = movie_name
        movie_item['date'] = movie_date
        movie_item['movie_type'] = movie_type
        yield movie_item
