from spider.db.redis_db import Urls
from spider.news.Duplicate import Duplicate

'''
redis 去重器，包含一级页面去重和二级页面去重
'''


class RedisDuplicate(Duplicate):
    def __init__(self, key_prefix):
        self.key_prefix = key_prefix

    def is_duplicate(self, url, is2level_page=False):
        if (is2level_page == True):
            result = Urls.is_crawled_2level_url(url)
        else:
            result = Urls.is_crawled_url(url, key=self.key_prefix + '_crawled_url')

        return result

    def put(self, url, is2level_page=False):
        if (is2level_page == True):
            Urls.store_crawled_2level_url(url)
        else:
            Urls.store_crawled_url(url, key=self.key_prefix + '_crawled_url')
