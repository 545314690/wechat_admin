# coding:utf-8
from spider.task.login import excute_login_task
import os

if __name__ == '__main__':
    # 由于celery的定时器有延迟，所以第一次需要手动
    excute_login_task()