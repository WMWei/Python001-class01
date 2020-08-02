# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from douban_comments.items import DoubanCommentsItem, DoubanMoviesItem

import pymysql


class DoubanMoviesCommentsPipeline:
    def open_spider(self, spider):
        print('开始运行')
        db = spider.settings.get('MYSQL_SCHEMAS', 'doubantop250')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'douban')
        psw = spider.settings.get('MySQL_PSW', 'douban')
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

    # 插入数据
    def insert_one(self, table, values_dict):
        keys, values = zip(*values_dict)
        sql = (
            f'INSERT INTO `{table}` '
            f'(`{"`,`".join(keys)}`) '
            f'VALUES ({", ".join("%s" for _ in keys)});'
        )
        self.cur.execute(sql, values)

    def process_item(self, item, spider):
        if isinstance(item, DoubanCommentsItem):
            table = spider.settings.get('MYSQL_TABLE').get('comments',
                                                           'comments')
        else:
            table = spider.settings.get('MYSQL_TABLE').get('movies', 'movies')

        self.insert_one(table, item.items())

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
        print('结束运行')




