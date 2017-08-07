# encoding=utf-8
import json
import os

import time
import wechat_admin.wsgi
from WeChatModel.admin import WeChatUserDao, KeywordDao
from spider.loggers.log import crawler as logger
from spider.service.common import *
from spider.task import wechat_crawl
from spider.task import keyword


# 获取总数
def get_total(kw, begin, count, name_cookies):
    response = search_by_page(kw, begin, count, name_cookies)
    max_num = response.json().get('total')
    return max_num


# 获取所有相关公众号
def fetch_all_url(kw, begin, count, name_cookies):
    # 先进行一次搜索并保存
    max_num = get_total(kw, begin, 1, name_cookies)
    while max_num > begin:
        search_url = get_search_biz_url(query=kw, begin=begin, count=count)
        logger.info(search_url)
        keyword.excute_user_crawl_task(search_url)
        begin += count


# 分页搜索并保存到数据库
def search_by_page(kw, begin, count, name_cookies):
    logger.info('开始search关键词=========>：' + str(begin) + ':' + kw)
    login_user = name_cookies[0]
    cookies = name_cookies[1]
    token = cookies['token']
    search_url = get_search_biz_url(query=kw, begin=begin, count=count, token=token)
    logger.info(search_url)
    search_response = requests.get(search_url, cookies=cookies, headers=header)
    return search_response


# 分页搜索并保存到数据库
def get_user_list(search_url):
    # 通过队列获取账号的cookie
    name_cookies = get_cookie()
    while name_cookies == None:
        logger.info('cookie 为空,60s后 重新获取')
        time.sleep(60)
        name_cookies = get_cookie()

    cookies = name_cookies[1]
    token = cookies['token']
    search_url = search_url + '&token=' + token
    logger.info("searching==========>:" + search_url)
    search_response = requests.get(search_url, cookies=cookies, headers=header)
    lists = search_response.json().get('list')
    for item in lists:
        json_str = json.dumps(item, ensure_ascii=False)
        logger.info(json_str)
        try:
            WeChatUserDao.create_by_json(item)
            #TODO:
            #触发爬取该用户url的任务,根据公众号的fakeid，即为biz
            logger.info("开始爬取公众号：" + item.get('nickname'))
            wechat_crawl.excute_wechat_user_crawl_task(item.get('fakeid'))
        except Exception as e:
            logger.error("保存公众号失败：" + json_str)
            logger.error(e)
    #执行完后休息一段时间
    random_time = random.randint(20, 50)
    time.sleep(random_time)

#
# if __name__ == '__main__':
#     get_user_list(
#         'https://mp.weixin.qq.com/cgi-bin/searchbiz?count=1&action=search_biz&query=datangleiyin&ajax=1&random=0.7103990078836312&lang=zh_CN&begin=0&f=json')
