# coding:utf-8
import time

from spider.db.redis_db import Cookies
from spider.task.workers import app
from spider.service import wechat_crawl
from spider.loggers.log import crawler

logger = crawler


# 爬取微信url
@app.task(ignore_result=True)
def wechat_url_crawl_task(search_url):
    wechat_crawl.get_article_url_list(search_url)


# 爬取微信文章
@app.task(ignore_result=True)
def wechat_crawl_task(url):
    wechat_crawl.get_article(url)


# 爬取微信url任务
def excute_wechat_url_crawl_task(search_url):
    app.send_task('spider.task.wechat_crawl.wechat_url_crawl_task', args=[search_url],
                  queue='wechat_url_crawl_task_queue')


# 爬取微信文章任务
def excute_wechat_crawl_task(url):
    app.send_task('spider.task.wechat_crawl.wechat_crawl_task', args=[url], queue='wechat_crawl_task_queue')
