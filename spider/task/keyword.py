# coding:utf-8
import time

from spider.task.workers import app
from spider.service import keyword, user_crawl
from spider.loggers.log import crawler

logger = crawler
from WeChatModel.admin import KeywordDao


@app.task(ignore_result=True)
def keyword_task(kw):
    logger.info('使用:' + kw + '爬取公众号信息')
    keyword.search_keyword(kw)


@app.task(ignore_result=True)
def excute_keyword_task():
    infos = KeywordDao.get_enable()
    logger.info('本次搜索关键词个数:' + str(len(infos)))
    for info in infos:
        kw = info.name
        logger.info('分发账号爬取任务:' + kw)
        app.send_task('spider.task.keyword.keyword_task', args=[kw], queue='search_keyword_queue')

#获取公众号列表任务
@app.task(ignore_result=True)
def user_list_crawl_task(search_url):
    user_crawl.get_user_list(search_url)


def excute_user_crawl_task(search_url):
    app.send_task('spider.task.keyword.user_list_crawl_task', args=[search_url], queue='user_list_crawl_queue')
