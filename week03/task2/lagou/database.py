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
        print(f'>>> <error>: 数据库连接失败! \n- 错误信息: {e}')
        return None


class MongoThread(Thread):
    def __init__(self,
                client: 'pymongo.MongoClient',
                data_queue: Queue):
        super().__init__()
        self.post = client[settings.MONGODB_DB][settings.MONGODB_COLNAME]
        self.data_queue = data_queue
        print(f'>>> 创建数据库写入线程<{self.name}>')

    def run(self):
        tools.lock_print(f'>>> 启动数据库写入线程<{self.name}>')
        while True:
            try:
                position_info = self.data_queue.get()
                if position_info is None:
                    break
                # 加锁，防止在判断到计数之间发生中断导致最终判断错误
                with tools.db_count_lock:
                    break_flag = self.upsert(position_info)
                # 若所有数据已满
                    if break_flag == 1:
                        break
                    # 如果某一个区域的目标数量已满足则跳过该条数据
                    if break_flag == 2:
                        continue
                
            except Exception as e:
                print(f'<{self.name}>:\n- <error>: 插入记录{position_info}到数据库失败\n- <error>: {e}')
            finally:
                self.data_queue.task_done()
        tools.lock_print(f'>>> 结束数据库写入线程<{self.name}>')

    def upsert(self, position_info: dict):
        if tools.check_db_position_count():
            return 1
        if tools.check_db_position_count(position_info['city']):
            return 2
        # 利用upsert去重
        res = self.post.update_one(
            filter={
                'position_name': position_info['position_name'],
                'city': position_info['city'],
                'salary': position_info['salary'],
                # 'company_id': position_info['company_id'],
            },
            update={
                '$set': {
                    'position_name': position_info['position_name'],
                    'city': position_info['city'],
                    'salary': position_info['salary'],
                },
            },
            upsert=True)
        if not res.matched_count == 1:
            # print(f'<{self.name}>: \n- 插入记录{position_info}到数据库中')
            tools.db_position_count.update([position_info['city']])
            tools.lock_print(f'<{self.name}>:\n- '
                            f'当前累计数量：{tools.db_position_count}')
        return 0



if __name__ == '__main__':
    # 测试数据库连接用
    connect_mongo()