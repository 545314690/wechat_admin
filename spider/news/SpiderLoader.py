# encoding=utf-8
import json
import re

from django.core import serializers

import wechat_admin.wsgi
import requests
from bs4 import BeautifulSoup

from NewsModel.admin import SiteDao
from NewsModel.models import Site
from spider.loggers.log import crawler
from spider.news.Spider import Spider
from spider.task import news_crawl


class SpiderLoader():
    def __init__(self):
        pass

    def load_all(self):
        site_list = SiteDao.get_enable()
        for site in site_list:
            self.start_site_task(site)

    def load_by_id(self, id):
        site = SiteDao.find_by_id(id).first()
        self.start_site_task(site)

    def start_site_task(self, site):
        news_crawl.excute_crawl_news_site_task(site.id, site.name)


if __name__ == '__main__':
    loader = SpiderLoader()
    # loader.load_all()
    loader.load_by_id('1')