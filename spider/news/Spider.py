# encoding=utf-8
import re

import wechat_admin.wsgi
import requests
from bs4 import BeautifulSoup

from NewsModel.models import Site, News
from spider.loggers.log import crawler
from spider.util.dateutil import DateUtil


class Spider():
    URL_SPLITTER = '\r\n'
    RULE_SPLITTER = ';'
    MIN_DETAIL_PAGE_TITLE_LEN = 6  # 最短详情页面title长度

    def __init__(self, site):
        self.site = site
        self.default_allow_domains = ['http://.*', 'https://.*']
        self.crawl_success_count = 0


        # 爬虫入口

    def start_crawl_site(self):
        start_urls = self.site.start_urls.split(Spider.URL_SPLITTER)

        for start_url in start_urls:
            self.crawl_site_url(start_url)

    # 去除指定标签
    def rm_tag(self, soup, tag):
        for s in soup(tag):
            s.extract()

    # 爬取单个链接
    def crawl_site_url(self, start_url):
        response = requests.get(start_url)
        soup = BeautifulSoup(response.content, 'lxml')
        urls = []
        if (self.site.url_rule_css):
            url_tags = soup.select(self.site.url_rule_css)
            crawler.info('共有url数量-->' + str(len(url_tags)))
            for url_tag in url_tags:
                try:
                    text = url_tag.get_text()
                    url = url_tag['href']
                    # TODO:
                    # len　函数需要修改，因为英文单词是按字母量计算的
                    if (len(text) > Spider.MIN_DETAIL_PAGE_TITLE_LEN):
                        if (self.is_allowed_url(url) == True):
                            if (len(text) > Spider.MIN_DETAIL_PAGE_TITLE_LEN):
                                # crawler.info('详情页-->' + text + '-->' + url)
                                self.crawl_detail(url)
                                # else:
                                # yield
                                # crawler.info('二级页面-->' + text + '-->' + url)
                                # urls.append(url)
                except Exception as e:
                    crawler.error(e)
        crawler.info('crawl_success_count : ' + str(self.crawl_success_count))

    def crawl_detail(self, detail_url):
        crawler.info('crawing page --> ' + detail_url)
        response = requests.get(detail_url)
        soup = BeautifulSoup(response.content, 'lxml')
        self.rm_tag(soup, 'script')
        self.rm_tag(soup, 'style')
        self.parse_page(soup, detail_url)

    def parse_page(self, soup, detail_url):
        title = self.parse_attr(soup, 'title')
        if (title == None):
            crawler.info('title none')
            return
        else:
            crawler.info('title-->' + title)
        pub_time = self.parse_attr(soup, 'pub_time')
        if (pub_time == None):
            crawler.info('pub_time none')
            return
        else:
            pub_time = DateUtil.cut_date_str(pub_time)
            crawler.info('pub_time-->' + pub_time)
        source = self.parse_attr(soup, 'source')
        if (source == None):
            crawler.info('source none')
            return
        else:
            crawler.info('source-->' + source)
        content = self.parse_attr(soup, 'content')
        if (content == None):
            crawler.info('content none')
            return
        else:
            crawler.debug('content-->' + content)

        comment_num = self.parse_attr(soup, 'comment_num')
        if (comment_num == None or comment_num == ''):
            comment_num = 0
            crawler.info('comment_num none')
        else:
            crawler.info('comment_num-->' + comment_num)
        # 保存数据
        news = News()
        news.site = self.site.name
        news.title = title.strip()
        news.url = detail_url
        news.pub_time = pub_time
        news.content = content
        news.source = source.strip()
        news.comment_num = comment_num
        news.save()
        self.crawl_success_count = self.crawl_success_count + 1

    def parse_title(self, soup):
        title = None
        if (self.site.title_rule_css):
            title_tag = soup.select_one(self.site.title_rule_css)
            if (title_tag):
                title = title_tag.get_text()
        elif self.site.title_rule_xpath:
            yield
        elif self.site.url_rule_reg:
            yield
        return title

    def parse_attr(self, soup, attr_name):

        attr = None
        attr_css_str = self.site.__getattribute__(attr_name + '_rule_css')
        if (attr_css_str):
            attr_css_rules = attr_css_str.split(Spider.RULE_SPLITTER)

            for attr_css in attr_css_rules:
                if (attr_css and attr_css != ''):
                    try:
                        attr_tag = soup.select_one(attr_css)
                        if (attr_tag):
                            attr = attr_tag.get_text()
                            break
                    # elif self.site.title_rule_xpath:
                    #     yield
                    # elif self.site.url_rule_reg:
                    #     yield
                    except Exception as e:
                        crawler.error(e)
                        crawler.error('error rule is : ' + attr_css)

        return attr

    def is_not_allowed_url(self, url):
        if (self.site.not_allowed_domains):
            not_allowed_domains = self.site.not_allowed_domains.split(Spider.URL_SPLITTER)
            for not_allowed_domain in not_allowed_domains:
                if (re.search(not_allowed_domain, url)):
                    return True

    def is_allowed_url(self, url):
        if (self.is_not_allowed_url(url)) == True:
            return False
        if (self.site.allow_domains == None):
            allow_domains = self.default_allow_domains
        else:
            allow_domains = self.site.allow_domains.split(Spider.URL_SPLITTER)
        for allow_domain in allow_domains:
            if (re.search(allow_domain, url)):
                return True
        return False


if __name__ == '__main__':
    site = Site()
    site.start_urls = 'http://news.sina.com.cn/'
    site.allow_domains = 'http://.*.sina.com.*'
    site.not_allowed_domains = 'http://video.*\r\nhttp://slide.*\r\nhttp://blog.*\r\nhttp://ent.*'
    site.url_rule_css = 'a'

    site.title_rule_css = '#artibodyTitle;#main_title;#j_title;div.LEFT  span > h1;body > div.transfer-warp > div.header > h1'
    site.pub_time_rule_css = '#navtimeSource;#pub_date;#page-tools > span > span.titer;#wrapOuter > div > div.page-info > span;span.article-a__time;div.LEFT  span > div.txtdetail'
    site.content_rule_css = '#artibody'
    site.source_rule_css = '#navtimeSource > span > span;#page-tools > span > span.source;#navtimeSource > span;#wrapOuter > div > div.page-info > span > span;#media_name;span.article-a__source;div.LEFT  span > div.txtdetail > a'
    site.comment_num_rule_css = '#commentCount1;a.tool-a__cmnt > em'
    spider = Spider(site)
    spider.start_crawl_site()
    #   div.LEFT  span > div.txtdetail > a

