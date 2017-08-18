import json

from spider.loggers.log import crawler
from spider.news.Pipeline import Pipeline
from spider.util.JsonUtil import CJsonEncoder


class JsonPipeline(Pipeline):
    def put(self, item):
        json_str = json.dumps(item, ensure_ascii=False,cls=CJsonEncoder)
        crawler.info(json_str)
        return item
