from wechat_admin import wsgi
import json

import datetime

from NewsModel.models import News
from spider.loggers.log import crawler
from spider.news.Pipeline import Pipeline
from spider.util.JsonUtil import CJsonEncoder


class ModelJsonPipeline(Pipeline):
    def put(self, item):
        json_str = json.dumps(item.to_dict(), ensure_ascii=False,cls=CJsonEncoder)
        crawler.info(json_str)
        return item

if __name__ == '__main__':
    jsonPipeline = ModelJsonPipeline()
    news = News()
    news.site = '新浪'
    news.date_created = datetime.datetime.now()
    jsonPipeline.put(news)