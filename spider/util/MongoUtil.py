# -*- coding: utf-8 -*-
from spider.config.conf import get_mongodb_conf

__author__ = 'lism'

from pymongo import MongoClient


class MongoUtil(object):
    conf = get_mongodb_conf()
    client = MongoClient(conf.get('host'), conf.get('port'))
    DB_NAME = conf.get('db');
    COLLECTION_NAME = 'news'
    db = client[DB_NAME]
    #db.authenticate(conf.get('user'), conf.get('pwd'))

    @staticmethod
    def get_db():
        return MongoUtil.client[MongoUtil.DB_NAME]

    @staticmethod
    def get_collection(collection=COLLECTION_NAME):
        return MongoUtil.get_db()[collection]

    @staticmethod
    def find(collection, *args):
        if (len(args) > 1):
            return MongoUtil.get_collection(collection).find(args[0], args[1])
        else:
            return MongoUtil.get_collection(collection).find(args[0])

    @staticmethod
    def save(collection, to_save):
        return MongoUtil.get_collection(collection).save(to_save)

    @staticmethod
    def delete(collection, to_delete):
        return MongoUtil.get_collection(collection).remove(to_delete)

    @staticmethod
    def count(collection, filter):
        return MongoUtil.get_collection(collection).count(filter)


if __name__ == '__main__':
    # MongoUtil.delete('crawllog',{})
    # result = MongoUtil.find('crawllog',{'level':'error'})
    result = MongoUtil.find('news', {})
    for rows in result:
        print(rows)

    count = MongoUtil.count('news',{})
    print(count)
