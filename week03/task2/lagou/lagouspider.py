from queue import Queue

import requests

import database
import crawls
import tools
import settings


@tools.cost_time
def run_spider():
    urls_queue = Queue()
    page_queue = Queue()
    data_queue = Queue()

    print(f'----开始运行爬虫----')
    # 创建要访问的url
    urls_iter = tools.gen_urls()
    for url in urls_iter:
        urls_queue.put(url)

    # 创建session
    session, search_headers = crawls.get_session()
    if session:
        request_threads = [crawls.RequestThread(session,
                                                search_headers,
                                                urls_queue,
                                                page_queue)
                            for c in range(settings.MAX_CONCURRENT)]
        parser_threads = [crawls.ParserThread(page_queue, data_queue)
                          for c in range(settings.MAX_CONCURRENT)]
        
        db_conn = database.connect_mongo()
        if db_conn:
            db_threads = [database.MongoThread(db_conn, data_queue)
                          for c in range(settings.MAX_CONCURRENT)]

            for r in request_threads:
                # r.setDaemon(True)
                r.start()
            for p in parser_threads:
                # p.setDaemon(True)
                p.start()
            for d in db_threads:
                # d.setDaemon(True)
                d.start()
                
            for r in request_threads:
                r.join()
            for p in parser_threads:
                p.join()
            for d in db_threads:
                d.join()
                # urls_queue.join()
                # page_queue.join()
                # data_queue.join()
            # 关闭数据库连接
            db_conn.close()
        # 关闭会话
        session.close()
    print(f'------运行结束------')
    print(f'-----获得记录数-----')
    print(tools.position_count_of_cities)


if __name__ == '__main__':
    run_spider()




