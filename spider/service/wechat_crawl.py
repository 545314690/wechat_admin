# encoding=utf-8
import json
import os

import time

from bs4 import BeautifulSoup

import wechat_admin.wsgi
from WeChatModel.admin import WeChatUserDao, KeywordDao
from WeChatModel.models import WeChatData
from spider.config.conf import get_url_save_path
from spider.db.redis_db import Urls
from spider.loggers.log import crawler as logger
from spider.service.common import *
from spider.task import wechat_crawl
from spider.util.DateUtil import timestamp_datetime
from spider.util.KafkaUtil import MyKafkaProducer
from spider.util.headers import header_wechat
from spider.util.json_util import class_to_dict

url_save_path = get_url_save_path()

# https://mp.weixin.qq.com/cgi-bin/appmsg?token=1975411548&lang=zh_CN&f=json&ajax=1&random=0.06881077661095647&action=list_ex&begin=0&count=50&query=&fakeid=MjM5MTM0NjQ2MQ%3D%3D&type=9
# 入口：获取所有相关文章
def fetch_user_all_url(wechat_biz):
    begin = 0
    count =50
    name_cookies = get_cookie()
    # 先进行一次搜索并保存
    max_num = get_total(wechat_biz, begin, 1, name_cookies)
    while max_num > begin:
        search_url = get_search_wechat_url(fakeid=wechat_biz, begin=begin, count=count)
        logger.info(search_url)

        # 发送搜索url任务
        wechat_crawl.excute_wechat_url_crawl_task(search_url)

        begin += count
    WeChatUserDao.set_history_crawled(wechat_biz)


# 获取总数
def get_total(wechat_user_id, begin, count, name_cookies):
    response = search_by_page(wechat_user_id, begin, count, name_cookies)
    max_num = response.json().get('app_msg_cnt')
    return max_num


# 分页搜索并保存到数据库
def search_by_page(wechat_biz, begin, count, name_cookies):
    logger.info('开始search公众号=========>：' + str(begin) + ':' + wechat_biz)
    login_user = name_cookies[0]
    cookies = name_cookies[1]
    token = cookies['token']
    search_url = get_search_wechat_url(fakeid=wechat_biz, begin=begin, count=count, token=token)
    logger.info(search_url)
    search_response = requests.get(search_url, cookies=cookies, headers=header)
    return search_response


# 分页搜索并保存到数据库
def get_article_url_list(search_url):
    # 通过队列获取账号的cookie
    name_cookies = get_cookie()
    while name_cookies == None:
        logger.info('cookie 为空,30s后 重新获取')
        time.sleep(30)
        name_cookies = get_cookie()

    cookies = name_cookies[1]
    token = cookies['token']
    search_url = search_url + '&token=' + token
    logger.info("searching article ==========>:" + search_url)
    search_response = requests.get(search_url, cookies=cookies, headers=header)
    lists = search_response.json().get('app_msg_list')

    if not os.path.exists(url_save_path):
        os.mkdir(url_save_path)
    urls_file = open(url_save_path + '/urls.txt', 'a+', encoding='utf-8')
    for item in lists:
        json_str = json.dumps(item, ensure_ascii=False)
        logger.info(json_str)
        try:
            link = item.get('link')
            # url写入文件
            urls_file.write(link + '\n')
            # 发送微信文章爬虫任务
            wechat_crawl.excute_wechat_crawl_task(link)

        except:
            logger.info("保存失败：" + json_str)

    urls_file.close()
    random_time = random.randint(15, 30)
    time.sleep(random_time)

def get_article(article_url):
    is_crawled = Urls.is_crawled_url(article_url)
    if(is_crawled == 1):
        logger.info("ignore crawled page : " + article_url)
        return
    logger.info("crawling page : " + article_url)
    response = requests.get(article_url, headers=header_wechat)
    soup = BeautifulSoup(response.content, 'lxml')
    html_str = str(soup)
    try:
        # article = soup.find('div', class_='rich_media')
        # title = article.find('h2').get_text()
        # meta_content = soup.find(id='meta_content')
        # time_str = meta_content.find(id='post-date').get_text()
        # nickname = meta_content.find_all('em')[1].get_text()
        content_div = soup.find(id='js_content')
        # content = content_div.get_text()
        content = str(content_div)
        msg_title = (re.search('(var msg_title = ")(.*)"', html_str).group(2))
        nickname = (re.search('(var nickname = ")(.*)"', html_str).group(2))
        alias = (re.search('(var user_name = ")(.*)"', html_str).group(2))
        publish_timestamp = (re.search('(var ct = ")(.*)"', html_str).group(2))
        publish_time = timestamp_datetime(publish_timestamp, type='s')
        # publish_time = time.localtime(int(publish_time_long))
        # publish_time = (re.search('(var publish_time = ")(.*)" ', html_str).group(2))
        round_head_img = (re.search('(var round_head_img = ")(.*)"', html_str).group(2))
        ori_head_img_url = (re.search('(var ori_head_img_url = ")(.*)"', html_str).group(2))
        msg_desc = (re.search('(var msg_desc = ")(.*)"', html_str).group(2))
        msg_source_url = (re.search('(var msg_source_url = \')(.*)\'', html_str).group(2))

        if msg_title:
            item = WeChatData()
            item.url = response.url
            item.title = msg_title
            item.nickname = nickname
            item.alias = alias
            item.pub_time = publish_time
            item.round_head_img = round_head_img
            item.ori_head_img_url = ori_head_img_url
            item.msg_desc = msg_desc
            item.msg_source_url = msg_source_url
            item.content = content
            # 文章处理
            try:
                dic = class_to_dict(item)
                del dic['_state']
                dic['date_modified'] = dic['date_created'] = timestamp_datetime(time.time(), type='s')
                # json_str = json.dumps(dic,ensure_ascii=False)
                # 发送到kafka(必须先发送到kafka，否则时间格式会让发送不成功)
                MyKafkaProducer.get_instance().send(dic)
                #保存到数据库
                WeChatData.save(item)
                Urls.store_crawled_url(article_url)
            except Exception as err:
                logger.error("保存微信文章异常：")
                logger.error(err)
                # dic = class_to_dict(item)
                # urls_file = open(url_save_path + '/articles.txt', 'a+', encoding='utf-8')
                # urls_file.writelines(str(dic) + '\n')
                # urls_file.close()
    except Exception as e:
        Urls.store_crawl_failed_url(article_url)
        logger.error(e)

# if __name__ == '__main__':
#     get_article(
#         'http://mp.weixin.qq.com/s?__biz=MzA3NjcwNjgyOQ==&mid=204671295&idx=3&sn=731238aecce2c638c3c1157092650e18#rd')
