import scrapy
from doubantop250.items import Doubantop250Item


class DoubanspiderSpider(scrapy.Spider):
    name = 'doubanspider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250/']

    #def parse(self, response):
    #    pass

    def start_requests(self):
        url = 'https://movie.douban.com/top250?start={}&filter='
        urls = (url.format(i * 25) for i in range(1))
        for link in urls:
            yield scrapy.Request(url=link, callback=self.list_parse)

    def list_parse(self, response):
        item = Doubantop250Item()
        links = response.xpath('//div[@class="hd"]/a/@href').getall()[:1]
        for link in links:
            item['link'] = link
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.info_parse)
    
    def info_parse(self, response):
        item = response.meta['item']
        movie_name = response.xpath('//div[@id="content"]/h1/span[1]/text()').get()
        print(movie_name)
        #movie_type = '/'.join(response.xpath('//div[@id="info"]/span[@[property="v:genre"]/text()').getall())
        #movie_date = '/'.join(response.xpath('//div[@id="info"]/span[@property="v:initialReleaseDate"]/text()').getall())
        #movie_rank = response.xpath('//div[@id="interest_sectl"]//strong[@class="ll rating_num"]/text()').get()
        item['name'] = movie_name
#        item['name'] = movie_name

        #item['m_type'] = 1
#       item['m_type'] = movie_type

        #item['date'] = 1
#        item['date'] = movie_date
        #item['rank'] = 1
#        item['rank'] = movie_rank
        yield item
