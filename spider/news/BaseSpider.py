# encoding=utf-8
import re

import wechat_admin.wsgi
import requests
from bs4 import BeautifulSoup

from NewsModel.models import Site
from spider.loggers.log import crawler


class Spider():
    def __init__(self, site):
        self.site = site

    def start_crawl_site(self):
        start_urls = self.site.start_urls.split('\n')
        for url in start_urls:
            self.crawl_site_url(url)

    def crawl_site_url(self, start_url):
        response = requests.get(start_url)
        soup = BeautifulSoup(response.content, 'lxml')
        urls = []
        if (self.site.url_rule_css):
            url_tags = soup.select(self.site.url_rule_css)
            crawler.info('共有url数量-->' + str(len(url_tags)))
            for url_tag in url_tags:
                text = url_tag.get_text()
                url = url_tag['href']
                if (self.is_allowed_url(url)):
                    if (len(text) > 6):
                        crawler.info('详情页-->' + text + '-->' + url)
                    else:
                        crawler.info('二级页面-->' + text + '-->' + url)
                    urls.append(url)

    def is_allowed_url(self, url):
        allow_domains = ['http://.*','https://.*']
        if (self.site.allow_domains):
            allow_domains = allow_domains + (self.site.allow_domains.split('\n'))
            for allow_domain in allow_domains:
                if (re.search(allow_domain, url)):
                    return True
            return False
        else:  # allow all domains
            return True


if __name__ == '__main__':
    site = Site()
    site.start_urls = 'http://news.sogou.com/'
    # site.allow_domains = 'http://news.sogou.com.*'
    site.url_rule_css = 'a'
    spider = Spider(site)
    spider.start_crawl_site()
