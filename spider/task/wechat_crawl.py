# coding:utf-8
import time

from spider.db.redis_db import Cookies
from spider.task.workers import app
from spider.service import wechat_crawl
from spider.loggers.log import crawler

logger = crawler


# 根据biz爬取微信公众号
@app.task(ignore_result=True)
def wechat_user_crawl_task(wechat_biz):
    wechat_crawl.fetch_user_all_url(wechat_biz)


# 爬取微信url
@app.task(ignore_result=True)
def wechat_url_crawl_task(search_url):
    wechat_crawl.get_article_url_list(search_url)


# 爬取微信文章
@app.task(ignore_result=True)
def wechat_crawl_task(url):
    wechat_crawl.get_article(url)


# 启动爬取微信公众号任务
def excute_wechat_user_crawl_task(wechat_biz):
    app.send_task('spider.task.wechat_crawl.wechat_user_crawl_task', args=[wechat_biz],
                  queue='wechat_user_crawl_queue')
# 启动爬取微信url任务
def excute_wechat_url_crawl_task(search_url):
    app.send_task('spider.task.wechat_crawl.wechat_url_crawl_task', args=[search_url],
                  queue='wechat_url_crawl_queue')


# 启动爬取微信文章任务
def excute_wechat_crawl_task(url):
    app.send_task('spider.task.wechat_crawl.wechat_crawl_task', args=[url], queue='wechat_crawl_queue')

if __name__ == '__main__':
    excute_wechat_crawl_task('https://mp.weixin.qq.com/s?__biz=MzAwNjYyNTI3MA==&mid=2650075694&idx=1&sn=06b566f80912b7c9869a5e392fe8c004&chksm=830ad0b7b47d59a13344e0d3798070744b822f4cc31b824b962bfc61da45be233d412c51422c&scene=21#wechat_redirect')