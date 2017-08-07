# encoding=utf-8
# from wechat_admin import wsgi
# from spider.db.redis_db import Urls
from spider.loggers.log import other
from spider.task import wechat_crawl


def push_to_redis(filename):
    file_seeds = open(filename, 'r', encoding='utf-8')
    for line in file_seeds:
        url = line.replace("\n", "")
        # other.info(url)
        # Urls.store_crawl_failed_url(url)
        wechat_crawl.excute_wechat_crawl_task(url)
    file_seeds.close()


if __name__ == '__main__':
    push_to_redis('/home/lism/urls/all_uniq.txt')
    # push_to_redis('/home/lism/urls/urls.txt')