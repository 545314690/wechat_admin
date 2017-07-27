import json
import random
import re
import time

import requests
from spider import headers

# from  spider.logger.logger import logger
from spider.logs.logger import logger
gzlist = []
file_seeds = open('../wechatuser/keyword.txt', 'r',encoding='utf-8')
for line in file_seeds:
    gzlist.append(line.replace("\n", ""))
logger.info(gzlist)
file_seeds.close()

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

def searchPage(kw, begin, count):
    logger.info('开始search关键词=========>：' + str(begin) + ':'+ kw)
    biz_file = open('biz/biz_' + kw + '.txt', 'a+', encoding='utf-8')
    biz_file_json = open('biz/biz_' + kw + '.json', 'a+', encoding='utf-8')
    query_id = {
        'action': 'search_biz',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'query': query,
        'begin': '{}'.format(str(begin)),
        'count': '5',
    }
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
    lists = search_response.json().get('list')
    max_num = search_response.json().get('total')
    for item in lists:
        json_str = json.dumps(item,ensure_ascii=False)
        logger.info(json_str)
        alias = item.get('alias')
        if alias == '':
            alias = item.get('nickname')
        biz_file.write(alias + '\n')
        biz_file.flush()
        biz_file_json.write(json_str + '\n')
        biz_file_json.flush()
    begin = int(begin)
    while max_num > begin:
        time.sleep(10)
        logger.info('翻页###################begin='+ str(begin))
        try:
            begin += 5
            searchPage(kw, begin, 5)
        except:
            logger.error('采集异常！！！！！！！')
    biz_file.flush()
    biz_file.close()
    biz_file_json.flush()
    biz_file_json.close()
for query in gzlist:
    searchPage(query, 265, 5)
    logger.info('完成采集公众号=========>：'+ query)
