import time

import datetime

from spider.util.MongoUtil import MongoUtil


class CrawlLog(object):
    def __init__(self, level='info',collection='crawllog'):
        self.collection = collection
        self.level = level
        pass

    def log(self, json):
        json['level'] = self.level
        json['date'] = datetime.datetime.now()
        MongoUtil.save(self.collection,json)

if __name__ == '__main__':
    log = CrawlLog(collection='aa')
    data = {'a':1,'aaa':datetime.datetime(2013, 2, 2, 1, 52, 12, 281000)}
    log.log(data)