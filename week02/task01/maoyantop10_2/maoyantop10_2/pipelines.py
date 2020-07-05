# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class Maoyantop102Pipeline:
    def open_spider(self, spider):
        db_cfg = {
            'host': 'localhost',
            'post': 3306,
            'user': 'root',
            'psw': 'HYb0A4D#NXMI&YVq'
            'db': 'Maoyantop10'
        }
        self.conn = pymysql.connect(
            host=db_cfg['host'],
            port=db_cfg['port'],
            user=db_cfg['user'],
            password=db_cfg['psw'],
            db=db_cfg['db']
        )

    def process_item(self, item, spider):
        
        try:
            sql = 'insert into maoyan(name, type, date) value (%s, %s, %s)'
            values = (
                item['name'],
                item['movie_type'],
                item['date']
            )
            self.conn.cursor().execute(sql, values)
            self.conn.commit()
        except:
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        self.conn.close()

