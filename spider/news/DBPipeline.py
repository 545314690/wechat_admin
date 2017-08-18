import json

from spider.news.Pipeline import Pipeline


class DBPipeline(Pipeline):
    def put(self, item):
        item.save()
        return item
