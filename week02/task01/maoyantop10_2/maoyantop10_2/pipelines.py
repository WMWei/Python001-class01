# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class Maoyantop102Pipeline:
    def open_spider(self, spider):
        db = spider.settings.get('MySQL_SCHEMAS','scrapy_demo')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'scrapy')
        psw = spider.settings.get('MySQL_PSW', '123456')
        charset = spider.settings.get('MYSQL_CHARSET', 'utf8mb4')

        self.db_conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=psw,
            db=db,
            charset=charset,
           )
        self.cur = self.db_conn.cursor()

    # 建表
    def create_table(self, name, field):
        field_str = ','.join(f'`{col}` CHAR(200)' for col in field)
        sql = (
            f'CREATE TABLE IF NOT EXISTS `{name}`'
            f'(`idx` INT UNSIGNED AUTO_INCREMENT,'
            f'{field_str},'
            f'PRIMARY KEY (`idx`)'
            f') ENGINE=InnoDB;'
        )
        self.cur.execute(sql)

    # 插入行
    def insert_one(self, table, values_dict):
        keys, values = zip(*values_dict.items())
        sql = (
            f'INSERT INTO `{table}` '
            f'(`{"`,`".join(keys)}`) '
            f'VALUES ({", ".join("%s" for _ in keys)});'
        )
        self.cur.execute(sql, values)

    def process_item(self, item, spider):
        infos = {
            'name': item['name'],
            'date': item['date'],
            'type': item['movie_type'],
        }
        table = spider.settings.get('MYSQL_TABLE', 'maoyantop10')
        self.create_table(table, infos.keys())
        self.insert_one(table, infos) 

        return item

    # 结束后关闭数据库
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

