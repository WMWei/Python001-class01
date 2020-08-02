import os
import sys

from scrapy import cmdline


root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)
os.chdir(root_dir)
cmdline.execute(['scrapy', 'crawl', 'douban'])