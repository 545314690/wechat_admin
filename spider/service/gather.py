import json
import re
import time
import sys
import requests
import random
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

gzlist = []
file_seeds = open('../wechatuser/mj.txt', 'r')
for line in file_seeds:
    gzlist.append(line.replace("\n", ""))
logger.info(gzlist)
file_seeds.close()
logger.info('读取seed成功')
url = 'https://mp.weixin.qq.com'
header = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
}

with open('cookie.txt', 'r', encoding='utf-8') as f:
    cookie = f.read()
cookies = json.loads(cookie)
response = requests.get(url=url, cookies=cookies)
token = re.findall(r'token=(\d+)', str(response.url))[0]
if (len(token) == 0):
    logger.error('cookie 无效，请重新登录获取cookie!')
    sys.exit(0)
for query in gzlist:
    logger.info('开始采集公众号=========>：' + query)
    urls_file = open('url/urls_' + query + '.txt', 'a+', encoding='utf-8')
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
        logger.info("未找到公众号:" + query)
        continue
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
        logger.info('翻页###################begin=' + str(begin))
        try:
            query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
            fakeid_list = query_fakeid_response.json().get('app_msg_list')
            for item in fakeid_list:
                logger.info(item.get('link'))
                urls_file.write(item.get('link') + '\n')
            num -= 1
            begin = int(begin)
            begin += 5
            time.sleep(random.randint(10,15))
        except:
            logger.error('采集异常！！！！！！！')
    urls_file.close()
    logger.info('完成采集公众号=========>：' + query)
