from queue import Queue, PriorityQueue

import requests

import database
import crawls
import tools
import settings


@tools.cost_time
def run_spider():
    urls_queue = Queue(20)
    page_queue = Queue(20)
    data_queue = Queue(300)

    print(f'----开始运行爬虫----')
    # 创建生产url线程
    sheduler_thread = crawls.ShedulerThread(urls_queue)

    # # 创建session
    # session, search_headers = crawls.get_session()
    # if session:
    request_threads = [crawls.RequestThread(#session,
                                            #search_headers,
                                            urls_queue,
                                            page_queue)
                      for c in range(settings.MAX_CONCURRENT)]
    parser_threads = [crawls.ParserThread(page_queue, data_queue)
                      for c in range(settings.MAX_CONCURRENT)]

    db_conn = database.connect_mongo()
    if db_conn:
        db_threads = [database.MongoThread(db_conn, data_queue)
                      for c in range(settings.MAX_CONCURRENT)]

        # 启动url生产
        sheduler_thread.start()
        # 启动页面请求
        for r in request_threads:
            # r.setDaemon(True)
            r.start()
        # 启动页面解析
        for p in parser_threads:
            # p.setDaemon(True)
            p.start()
        # 启动数据库存储
        for d in db_threads:
            # d.setDaemon(True)
            d.start()

        sheduler_thread.join()

        # 等待队列输出
        urls_queue.join()
        page_queue.join()
        data_queue.join()
        # 输入队列结束标记
        for r in request_threads:
            urls_queue.put(None)
        for p in parser_threads:
            page_queue.put(None)
        for d in db_threads:
            data_queue.put(None)

        for r in request_threads:
                r.join()
        for p in parser_threads:
            p.join()
        for d in db_threads:
            d.join()
        
        # 关闭数据库连接
        db_conn.close()
        # 关闭会话
        # session.close()
    print(f'------运行结束------')
    print(f'-----获得记录数-----')
    print(dict(tools.db_position_count))


if __name__ == '__main__':
    run_spider()




