# encoding=utf-8
import re

import wechat_admin.wsgi
import requests
from bs4 import BeautifulSoup

from NewsModel.admin import SiteDao
from NewsModel.models import Site, News
from spider.loggers.log import crawler
from spider.news.CrawlLog import CrawlLog
from spider.news.DBPipeline import DBPipeline
from spider.news.ModelJsonPipeline import ModelJsonPipeline
from spider.news.MongoPipeline import MongoPipeline
from spider.news.RedisDuplicate import RedisDuplicate
from spider.task import news_crawl
from spider.util.dateutil import DateUtil


class Spider():
    name = 'news'
    URL_SPLITTER = '\r\n'
    RULE_SPLITTER = ';'
    MIN_2LEVEL_PAGE_TITLE_LEN = 2  # 最短二级页面title长度
    MIN_DETAIL_PAGE_TITLE_LEN = 7  # 最短详情页面title长度
    pipelines = []
    duplicate = None
    timeout = (3, 5)
    error_log = CrawlLog('error')
    success_log = CrawlLog('info')

    def __init__(self, site):
        self.site = site
        self.default_allow_domains = ['http://.*', 'https://.*']
        self.crawl_success_count = 0
        self.add_pipelines()
        self.add_duplicate()

    '''
    爬虫入口
    '''

    def start_crawl_site(self, start_page=None, deep=1):
        if (start_page == None):
            start_urls = self.site.start_urls.split(Spider.URL_SPLITTER)
        else:
            start_urls = start_page.split(Spider.URL_SPLITTER)
        for start_url in start_urls:
            self.crawl_site_url(start_url, deep)

    '''
    添加去重器
    '''

    def add_duplicate(self):
        duplicate = RedisDuplicate(self.name)
        self.duplicate = duplicate

    '''
    添加管道处理器
    '''

    def add_pipelines(self):
        # json_pipeline = ModelJsonPipeline()
        db_pipeline = DBPipeline()
        mongo_pipeline = MongoPipeline(self.name)

        # self.pipelines.append(json_pipeline)
        self.pipelines.append(db_pipeline)
        self.pipelines.append(mongo_pipeline)

    '''
    数据放入管道
    '''

    def put_to_pipelines(self, item):
        for pipe in self.pipelines:
            item = pipe.put(item)
        return item

    '''
    去除指定标签
    '''

    def rm_tag(self, soup, tag):
        for s in soup(tag):
            s.extract()

    '''
    爬取单个链接
    '''

    def crawl_site_url(self, start_url, deep):
        #如果达到最大抓取深度或者该二级页面被重复抓取过就返回
        if (deep > self.site.crawl_deep):
            return
        #如果不是第一层链接，并且被抓取过
        if(deep !=1 and self.duplicate.is_duplicate(start_url, is2level_page=True) == True):
            crawler.info('ignore crawled [' + self.site.name + '] 第' + str(deep) + '层页面 ' + start_url)
            return
        crawler.info('crawling [' + self.site.name + '] 第' + str(deep) + '层页面 ' + start_url)
        try:
            response = requests.get(start_url, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'lxml')
        except Exception as exc :#如果爬虫出错，加入重试
            raise news_crawl.crawl_site_2level_page_task.retry(exc=exc)
        # 放入抓取过的列表中
        self.duplicate.put(start_url, is2level_page=True)
        urls = []
        if (self.site.url_rule_css):
            url_tags = soup.select(self.site.url_rule_css)
            crawler.info('parsed [' + self.site.name + '] 第' + str(deep) + '层页面 ' + start_url + ' 共有url数量-->' + str(len(url_tags)))
            for url_tag in url_tags:
                try:
                    text = url_tag.get_text()
                    url = url_tag['href']
                    # TODO:
                    # len　函数需要修改，因为英文单词是按字母量计算的
                    text_len = len(text.strip())
                    if (self.is_allowed_url(url) == True):
                        '''
                        详情页
                        '''
                        if (text_len >= Spider.MIN_DETAIL_PAGE_TITLE_LEN):

                            # 判断是否抓取过
                            if (self.duplicate.is_duplicate(url) == False):
                                #TODO:把详情页的爬取放入任务队列
                                self.crawl_detail(url)
                            else:
                                crawler.info('ignore crawled　page : ' + url)
                        elif (text_len >= Spider.MIN_2LEVEL_PAGE_TITLE_LEN):
                            '''
                            二级页面,deep+1
                            '''
                            # 判断是否超出最大爬取层数
                            if (deep + 1 <= self.site.crawl_deep):
                                # 判断是否是合法的url,是否抓取过
                                if (self.duplicate.is_duplicate(url, is2level_page=True) == False):

                                    # self.crawl_site_url(url, deep + 1)
                                    # crawler.info('sending crawl　2level page task: ' + url)
                                    # news_crawl.excute_crawl_site_2level_page_task(self.site.id, self.site.name, url, deep + 1)
                                    pass

                            else:
                                crawler.info('ignore crawled [' + self.site.name + '] 第' + str(deep) + '层页面 ' + url)
                        else:
                            crawler.info('ignore too short title page : ' + url)
                    else:
                        crawler.info('ignore not allowed page : ' + url)
                except Exception as e:
                    self.error_log.log(
                        {'msg': 'crawl 2level page error', 'url': start_url, 'site': self.site.name, 'main_name': self.site.main_name, 'deep': deep})
                    crawler.error(e)
            self.success_log.log({'msg': 'success', 'url': start_url, 'site': self.site.name, 'main_name': self.site.main_name, 'deep': deep})
        crawler.info('crawl_success_count : ' + str(self.crawl_success_count))

    '''
    爬取详情页
    '''

    def crawl_detail(self, detail_url):
        crawler.info('crawing page --> ' + detail_url)
        response = requests.get(detail_url, timeout=self.timeout)
        soup = BeautifulSoup(response.content, 'lxml')
        self.rm_tag(soup, 'script')
        self.rm_tag(soup, 'style')
        self.parse_page(soup, detail_url)

    '''
    解析页面
    '''

    def parse_page(self, soup, detail_url):
        title = self.parse_attr(soup, 'title')
        if (title == None):
            crawler.info('title none')
            self.error_log.log({'msg': 'title', 'url': detail_url, 'site': self.site.name, 'main_name': self.site.main_name})
            return
        else:
            crawler.info('title-->' + title)
        pub_time = self.parse_attr(soup, 'pub_time')
        if (pub_time == None):
            crawler.info('pub_time none')
            self.error_log.log({'msg': 'pub_time', 'url': detail_url, 'site': self.site.name, 'main_name': self.site.main_name})
            return
        else:
            pub_time = DateUtil.cut_date_str(pub_time)
            crawler.info('pub_time-->' + pub_time)
        source = self.parse_attr(soup, 'source')
        if (source == None):
            crawler.info('source none')
            self.error_log.log({'msg': 'source', 'url': detail_url, 'site': self.site.name, 'main_name': self.site.main_name})
            # return
        else:
            crawler.info('source-->' + source)
        content = self.parse_attr(soup, 'content')
        if (content == None):
            crawler.info('content none')
            self.error_log.log({'msg': 'content', 'url': detail_url, 'site': self.site.name, 'main_name': self.site.main_name})
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
        if(self.site.main_name):
            news.site = self.site.main_name
        else:
            news.site = self.site.name
        news.title = title.strip()
        detail_url = detail_url.strip()
        news.url = detail_url
        news.pub_time = pub_time
        news.content = content.strip()
        news.source = source.strip()
        news.comment_num = comment_num
        # 放入管道
        self.put_to_pipelines(news)

        # 放入去重器
        self.duplicate.put(detail_url)
        self.crawl_success_count = self.crawl_success_count + 1
        self.success_log.log({'msg': 'success', 'url': detail_url, 'site': self.site.name, 'main_name': self.site.main_name})

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

    '''
    根据属性名解析屬性
    '''

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
                            if attr and attr != '':
                                break
                    # elif self.site.title_rule_xpath:
                    #     yield
                    # elif self.site.url_rule_reg:
                    #     yield
                    except Exception as e:
                        crawler.error(e)
                        crawler.error('error rule is : ' + attr_css)
        if attr and attr != '':
            return attr
        else:
            return None

    '''
    判定是否是不允许爬取的url
    '''

    def is_not_allowed_url(self, url):
        if (self.site.not_allowed_domains):
            not_allowed_domains = self.site.not_allowed_domains.split(Spider.URL_SPLITTER)
            for not_allowed_domain in not_allowed_domains:
                if (re.search(not_allowed_domain, url)):
                    return True

    '''
        判定是否是允许爬取的url
    '''

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
    # site = Site()
    # site.name = '新浪新闻'
    # site.start_urls = 'http://news.sina.com.cn/'
    # site.allow_domains = 'http://.*.sina.com.*'
    # site.not_allowed_domains = 'http://video.*\r\nhttp://slide.*\r\nhttp://blog.*\r\nhttp://ent.*'
    # site.url_rule_css = 'a'
    #
    # site.title_rule_css = '#artibodyTitle;#main_title;#j_title;div.LEFT  span > h1;body > div.transfer-warp > div.header > h1'
    # site.pub_time_rule_css = '#navtimeSource;#pub_date;#page-tools > span > span.titer;#wrapOuter > div > div.page-info > span;span.article-a__time;div.LEFT  span > div.txtdetail'
    # site.content_rule_css = '#artibody'
    # site.source_rule_css = '#navtimeSource > span > span;#page-tools > span > span.source;#navtimeSource > span;#wrapOuter > div > div.page-info > span > span;#media_name;span.article-a__source;div.LEFT  span > div.txtdetail > a'
    # site.comment_num_rule_css = '#commentCount1;a.tool-a__cmnt > em'


    site = SiteDao.find_by_id(7).first()
    spider = Spider(site)
    spider.start_crawl_site()
