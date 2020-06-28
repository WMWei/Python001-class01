# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class Maoyantop10Pipeline:
    def process_item(self, item, spider):
        movie_name = item['name']
        movie_type = item['movie_type']
        movie_date = item['date']
        movies = pd.DataFrame(data=[[movie_name, movie_type, movie_date],])
        movies.to_csv('./maoyantop10.csv', mode='a', index=False, header=False)
        return item
