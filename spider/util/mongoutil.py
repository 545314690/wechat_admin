# -*- coding: utf-8 -*-
__author__ = 'lism'

from pymongo import MongoClient

class MongoUtil:
    connection = MongoClient("192.168.0.2",27007)
    DB_NAME = 'test';
    COLLECTION_NAME = 'news'
    @staticmethod
    def get_db():
        return MongoUtil.connection[MongoUtil.DB_NAME]

    @staticmethod
    def get_collection():
        return MongoUtil.get_db()[MongoUtil.COLLECTION_NAME]

    @staticmethod
    def find(*args):
        if(len(args) > 1 ):
            return MongoUtil.get_collection().find(args[0],args[1])
        else:
            return MongoUtil.get_collection().find(args[0])
    @staticmethod
    def save(to_save):
        return MongoUtil.get_collection().save(to_save)

    @staticmethod
    def delete(to_delete):
        return MongoUtil.get_collection().remove(to_delete)