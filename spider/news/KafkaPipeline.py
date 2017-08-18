import json

from spider.loggers.log import crawler
from spider.news.Pipeline import Pipeline


class KafkaPipeline(Pipeline):
    def put(self, item):
        return item
