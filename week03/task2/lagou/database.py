from threading import Thread
from queue import Queue

import pymongo

import settings
import tools 


# MONGODB数据库连接
def connect_mongo():
    try:
        print('>>> 正在连接数据库...')
        client = pymongo.MongoClient(host=settings.MONGODB_HOST,
                                    port=settings.MONGODB_PORT,
                                    username=settings.MONGODB_USER,
                                    password=settings.MONGODB_PSW,
                                    authSource=settings.MONGODB_DB,
                                    )
        print('>>> 数据库连接成功!')
        return client
    except Exception as e:
        print(f'>>> 数据库连接失败!')
        print(e)
        return None


class MongoThread(Thread):
    def __init__(self,
                client: 'pymongo.MongoClient',
                data_queue: Queue):
        super().__init__()
        self.post = client[settings.MONGODB_DB][settings.MONGODB_COLNAME]
        self.data_queue = data_queue
        print(f'>>> 创建数据库写入进程{self.name}')

    def run(self):
        print(f'>>> 启动数据库写入进程{self.name}')
        while True:
            # 加锁，防止在插入数据库操作进行，但累计记录数量未执行时，中断到另外的数据库操作线程，导致最终结果多于需求的记录数量
            # 另一方面也避免错误的计数
            with tools.count_lock:
                if tools.check_position_count():
                    break
                try:
                    position_info = self.data_queue.get()
                    if tools.check_position_count(position_info['city']):
                        continue
                    self.upsert(position_info)
                except Exception as e:
                    print(f'{self.name}: 插入记录{position_info}到数据库失败')
                finally:
                    self.data_queue.task_done()
        print(f'>>> 结束数据库写入进程{self.name}')

    def upsert(self, position_info: dict):
        
        # 利用mongodb的upsert去重和插入
        result = self.post.update_one(
            filter={
                'position_name': position_info['position_name'],
                'city': position_info['city'],
                'salary': position_info['salary'],
                'company_id': position_info['company_id'],
            },
            update={
                '$set': {
                    'position_name': position_info['position_name'],
                    'position_id': position_info['position_id'], 
                    'city': position_info['city'],
                    'created': position_info['created'],
                    'salary': position_info['salary'],
                    'company_id': position_info['company_id'],
                    'company': position_info['company'],
                    'company_full_name': position_info['company_full_name'],
                }
            },
            upsert=True)
        if result.matched_count == 0:
            print(f'{self.name}: 插入记录{position_info}到数据库中')
            tools.position_count(position_info['city'])



if __name__ == '__main__':
    # 测试数据库连接用
    connect_mongo()