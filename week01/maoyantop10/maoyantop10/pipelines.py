# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class Maoyantop10Pipeline:
    def open_spider(self, spider):
        self.f = open('./maoyantop10.csv', 'a', encoding='utf-8')
        self.writer = csv.DictWriter(self.f, fieldnames=[
            '电影',
            '类型',
            '日期',
            '链接'
        ])
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow({
            '电影': item['name'],
            '类型': item['movie_type'],
            '日期': item['date'],
            '链接': item['link']
        })
        return item

    def close_spider(self, spider):
        self.f.close()
