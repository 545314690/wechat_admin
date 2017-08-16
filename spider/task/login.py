# coding:utf-8
import time

from spider.db.redis_db import Cookies
from spider.task.workers import app
from spider.service.login import do_wechat_login
from spider.loggers.log import logger

from WeChatModel.admin import LoginUserDao


@app.task(ignore_result=True)
def login_task(name, password):
    do_wechat_login(name, password)


def batch_login():
    """
    通过本地调用相关账号进行登录，该方法可能会有用
    """
    infos = LoginUserDao.get_enable()
    for info in infos:
        login_task(info.name, info.password, info.need_verify)
        time.sleep(10)


# worker设置并发数为1，所以可以通过sleep()限制不同账号登录速度，账号登录速度过快，ip会被微博系统设定为异常ip
@app.task(ignore_result=True)
def excute_login_task():
    infos = LoginUserDao.get_enable()
    print(infos)
    # 每次登陆前清楚所有堆积的登录任务
    Cookies.check_login_task()
    logger.info('本轮模拟登陆开始')
    for info in infos:
        app.send_task('spider.task.login.login_task', args=(info.name, info.password), queue='login_queue')
        # routing_key='for_login')
        time.sleep(10)

if __name__ == '__main__':
    excute_login_task()