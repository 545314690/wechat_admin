# encoding=utf-8
import os


import json
import random
import re
import time

import django
import requests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wechat_admin.settings")  # project_name 项目名称
django.setup()
from WeChatModel.admin import WeChatUserDao, KeywordDao
from WeChatModel.models import WeChatUser
from spider.db.redis_db import Cookies
from spider.loggers.log import crawler as logger

url = 'https://mp.weixin.qq.com'
header = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
}


def get_token(name_cookies):
    login_user = name_cookies[0]
    cookies = name_cookies[1]
    response = requests.get(url=url, cookies=cookies)
    response_list = re.findall(r'token=(\d+)', str(response.url))
    if (len(response_list)):
        token = response_list[0]
        return token
    else:
        return None


def search_keyword(kw):
    # 通过队列获取账号的cookie
    name_cookies = Cookies.fetch_cookies()
    if (len(name_cookies) == 0):
        logger.error("没有可用cookie。")
    else:
        token = get_token(name_cookies)
        fetch_all(kw, 0, 5, name_cookies, token)
        logger.info('完成搜索公众号=========>关键词：' + kw)
        # 设置为不可用
        KeywordDao.set_enable(kw, False)


# 获取总数
def get_total(kw, begin, count, name_cookies, token):
    max_num = search_by_page(kw, begin, count, name_cookies, token).get('total')
    return max_num


# 获取所有相关公众号
def fetch_all(kw, begin, count, name_cookies, token):
    #先进行一次搜索并保存
    max_num = get_total(kw, begin, count, name_cookies, token)
    while max_num > begin:
        time.sleep(random.randint(10, 15))
        logger.info('翻页###################begin=' + str(begin))
        try:
            begin += count
            search_by_page(kw, begin, count, name_cookies, token)
        except:
            logger.error('采集异常！！！！！！！')


# 分页搜索并保存到数据库
def search_by_page(kw, begin, count, name_cookies, token):
    logger.info('开始search关键词=========>：' + str(begin) + ':' + kw)
    login_user = name_cookies[0]
    cookies = name_cookies[1]
    query_id = {
        'action': 'search_biz',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'query': kw,
        'begin': '{}'.format(str(begin)),
        'count': count,
    }
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
    lists = search_response.json().get('list')
    for item in lists:
        json_str = json.dumps(item, ensure_ascii=False)
        logger.info(json_str)
        try:
            WeChatUserDao.create_by_json(item)
        except:
            logger.info("保存失败："+json_str)
    return search_response.json()
#
#
# if __name__ == '__main__':
#     search_keyword('安全生产')