import random
import re
import time

import requests

# Get an instance of a logger
from WeChatModel.admin import WeChatUserDao
from spider.config.conf import get_url_save_path
from spider.db.redis_db import Cookies
from spider.loggers.log import crawler

url = 'https://mp.weixin.qq.com'
header = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
}

url_save_path = get_url_save_path()


def gather_wechat_user(wechat_user_id):
    # 通过队列获取账号的cookie
    name_cookies = Cookies.fetch_cookies()
    if (len(name_cookies) == 0):
        crawler.error("没有可用cookie。")
    else:
        get_wechat_user_urls(wechat_user_id, name_cookies)


def get_wechat_user_urls(wechat_user_id, name_cookies):
    login_user = name_cookies[0]
    cookies = name_cookies[1]
    response = requests.get(url=url, cookies=cookies)
    response_list = re.findall(r'token=(\d+)', str(response.url));
    if (len(response_list)):
        token = response_list[0]
        query = wechat_user_id
        crawler.info('使用账号[' + login_user + ']开始采集公众号=========>：' + query)
        urls_file = open(url_save_path + '/urls_' + query + '.txt', 'a+', encoding='utf-8')
        query_id = {
            'action': 'search_biz',
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': query,
            'begin': '0',
            'count': '5',
        }
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
        lists = search_response.json().get('list')
        if (len(lists) == 0):
            crawler.info("未找到公众号:" + query)
        else:
            fakeid = lists[0].get('fakeid')
            query_id_data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '0',
                'count': '5',
                'query': '',
                'fakeid': fakeid,
                'type': '9'
            }
            appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
            appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
            max_num = appmsg_response.json().get('app_msg_cnt')
            num = int(int(max_num) / 5)
            begin = 0
            while num + 1 > 0:
                query_id_data = {
                    'token': token,
                    'lang': 'zh_CN',
                    'f': 'json',
                    'ajax': '1',
                    'random': random.random(),
                    'action': 'list_ex',
                    'begin': '{}'.format(str(begin)),
                    'count': '5',
                    'query': '',
                    'fakeid': fakeid,
                    'type': '9'
                }
                crawler.info('翻页###################begin=' + str(begin))
                try:
                    query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header,
                                                         params=query_id_data)
                    fakeid_list = query_fakeid_response.json().get('app_msg_list')
                    for item in fakeid_list:
                        crawler.info(item.get('link'))
                        urls_file.write(item.get('link') + '\n')
                    urls_file.flush()
                    num -= 1
                    begin = int(begin)
                    begin += 5
                    time.sleep(random.randint(10, 15))
                except:
                    crawler.error('采集异常！！！！！！！')
            urls_file.close()
            crawler.info('完成采集公众号=========>：' + query)
            WeChatUserDao.set_history_crawled(query)
    else:
        crawler.info(login_user + 'cookie 失效，请重新登录,正在删除...')
        Cookies.delete_cookies(login_user)
        crawler.info(login_user + 'cookie，删除成功。')


# gather_wechat_user('gjyjzx')
