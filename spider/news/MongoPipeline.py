import json

from spider.loggers.log import crawler
from spider.news.Pipeline import Pipeline
from spider.util.MongoUtil import MongoUtil


class MongoPipeline(Pipeline):
    def __init__(self, collection):
        self.collection = collection

    def put(self, item):
        json_obj = item.to_dict()
        MongoUtil.save(self.collection, json_obj)
        return item
