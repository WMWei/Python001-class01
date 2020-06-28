import os
import sys
from scrapy import cmdline

base_dir = os.path.dirname(os.path.abspath('__file__'))  # 项目根目录
sys.path.append(base_dir)  # 加入环境变量
os.chdir(base_dir)  # 切换工作目录
cmdline.execute(['scrapy', 'crawl', 'maoyanspider'])
