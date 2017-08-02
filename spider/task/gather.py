# coding:utf-8
import time

from spider.task.workers import app
from spider.service import gather
from spider.loggers.log import crawler

logger = crawler
from WeChatModel.admin import WeChatUserDao


@app.task(ignore_result=True)
def history_task(account):
    logger.info('接受账号爬取任务:' + account)
    gather.gather_wechat_user(account)


@app.task(ignore_result=True)
def excute_crawl_history_task():
    infos = WeChatUserDao.get_enable_and_history_not_crawled();
    logger.info('本次爬取账号个数:' + str(len(infos)))
    for info in infos:
        account = info.alias
        if (account == None or account == ''):
            account = info.nickname
        logger.info('分发账号爬取任务:' + account)
        app.send_task('spider.task.gather.history_task', args=[account], queue='crawl_history_queue')
            # routing_key='for_login')