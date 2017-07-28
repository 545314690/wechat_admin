# coding:utf-8
from spider.task.gather import excute_crawl_history_task
import os

if __name__ == '__main__':
    # 由于celery的定时器有延迟，所以第一次需要手动
    excute_crawl_history_task()