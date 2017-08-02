# encoding=utf-8
import wechat_admin.wsgi
from WeChatModel.admin import KeywordDao
from spider.loggers.log import crawler as logger
from spider.service import user_crawl
from spider.service.common import *

page_size = 10
start = 0


def search_keyword(kw):
    # 通过队列获取账号的cookie
    name_cookies = get_cookie()
    while name_cookies == None:
        logger.info('搜索关键词' + kw + '时,cookie 为空,重新获取')
        name_cookies = get_cookie()
    user_crawl.fetch_all_url(kw, start, page_size, name_cookies)
    logger.info('搜索公众号任务完成=========>关键词：' + kw)
    # 设置为不可用
    KeywordDao.set_enable(kw, False)

# if __name__ == '__main__':
#
#     search_keyword('datangleiyin')