# encoding=utf-8
import random
import re
import requests

from spider.db.redis_db import Cookies
from spider.loggers.log import logger

url = 'https://mp.weixin.qq.com'
base_search_biz_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz'
base_search_wechat_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
header = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
}


def get_cookie():
    # 通过队列获取账号的cookie
    name_cookies = Cookies.fetch_cookies()
    if (name_cookies != None and len(name_cookies) != 0):
        return name_cookies
    else:
        logger.error("没有可用cookie。")
        return None


def get_token_by_cookies(cookies):
    if (cookies != None):
        response = requests.get(url=url, cookies=cookies)
        response_list = re.findall(r'token=(\d+)', str(response.url))
        if (len(response_list)):
            token = response_list[0]
            return token
    return None


def get_token(name_cookies):
    if (name_cookies != None):
        login_user = name_cookies[0]
        cookies = name_cookies[1]
        response = requests.get(url=url, cookies=cookies)
        response_list = re.findall(r'token=(\d+)', str(response.url))
        if (len(response_list)):
            token = response_list[0]
            return token
    return None


def get_request_url(base_url, params):
    param_list = []
    for key in params:
        param_list.append(str(key) + '=' + str(params[key]))
    request_url = base_url + "?" + "&".join(param_list)
    return request_url

#得到搜索公众号的链接
def get_search_biz_url(query='', begin=0, count=10, token=None):
    default = {
        'action': 'search_biz',
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'query': '',
        'begin': '{}'.format(str(0)),
        'count': 10
    }
    default['query'] = query
    default['begin'] = '{}'.format(str(begin))
    default['count'] = '{}'.format(str(count))
    if (token != None):
        default['token'] = token
    return get_request_url(base_search_biz_url, default)

#得到搜索文章的链接
def get_search_wechat_url(fakeid='', begin=0, count=50, token=None):
    default = {
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',
        'count': '50',
        'fakeid': '',  # 公众号的biz
        'query': '',  # 文章关键词搜索，这里写空，代表搜索所有文章
        'type': '9'
    }
    default['fakeid'] = fakeid
    default['begin'] = '{}'.format(str(begin))
    default['count'] = '{}'.format(str(count))
    if (token != None):
        default['token'] = token
    return get_request_url(base_search_wechat_url, default)
