# encoding=utf-8
import re

import wechat_admin.wsgi
import requests
from bs4 import BeautifulSoup

from NewsModel.admin import SiteDao
from NewsModel.models import Site
from spider.loggers.log import crawler
from spider.news.Spider import Spider


class SpiderLoader():
    def __init__(self):
        pass

    def load_all(self):
        site_list = SiteDao.get_enable()
        for site in site_list:
            self.start_site_task(site)

    def start_site_task(self, site):
        spider = Spider(site)
        spider.start_crawl_site()


if __name__ == '__main__':
    loader = SpiderLoader()
    loader.load_all()