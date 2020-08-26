import os
import sys

from scrapy import cmdline


base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
os.chdir(base_dir)
cmdline.execute(['scrapy', 'crawl', 'smzdm_comments'])