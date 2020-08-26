# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from smzdm.items import ProductItem, CommentItem

import pymysql


class SmzdmPipeline:
    def open_spider(self, spider):
        print('开始运行爬虫')
        db = spider.settings.get('MYSQL_SCHEMAS', 'smzdm')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'smzdm')
        psw = spider.settings.get('MYSQL_PSW', 'smzdm')
        charset = spider.settings.get('MYSQL_CHARSET', 'utf8mb4')

        self.conn = pymysql.Connection(
            host=host,
            port=port,
            user=user,
            password=psw,
            db=db,
            charset=charset,
        )
        self.cur = self.conn.cursor()
        # 取消外键约束防止插入失败
        self.cur.execute('SET FOREIGN_KEY_CHECKS=0;')

    def insert_one(self, table, values_dict):
        keys, values = zip(*values_dict)
        sql = (
            f'INSERT INTO `{table}` '
            f'(`{"`,`".join(keys)}`) '
            f'VALUES ({", ".join("%s" for _ in keys)});'
        )
        self.cur.execute(sql, values)

    def process_item(self, item, spider):
        if isinstance(item, ProductItem):
            table = spider.settings.get('MYSQL_TABLE').get('products', 'products')
        else:
            table = spider.settings.get('MYSQL_TABLE').get('comments', 'comments')
        
        self.insert_one(table, item.items())

        return item
    
    def close_spider(self, spider):
        # 执行完毕恢复约束
        self.cur.execute('SET FOREIGN_KEY_CHECKS=1;')
        self.conn.commit()
        self.conn.close()
        print('结束运行')
