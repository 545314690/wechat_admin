# encoding:utf-8
from wechat_admin import wsgi
from spider.news import Spider
from NewsModel.admin import SiteDao
from spider.task.workers import app


@app.task(ignore_result=True)
def crawl_site_task(site_id, site_name):
    # 从数据库查询site
    site = SiteDao.find_by_id(site_id).first()
    # 开始爬虫此站点
    spider = Spider.Spider(site)
    spider.start_crawl_site()


@app.task(ignore_result=True)
def excute_crawl_news_site_task(site_id, site_name):
    app.send_task('spider.task.news_crawl.crawl_site_task', args=[site_id, site_name],
                  queue='crawl_news_site_queue')


@app.task(ignore_result=True)
def crawl_site_2level_page_task(site_id, site_name, url, deep):
    # 这里要对二级页面去重，防止重复抓取。又不能完全去重，需要设置爬取过的页面的过期时间，比如1个小时内不再抓取爬过的二级页面
    # 从数据库查询site
    site = SiteDao.find_by_id(site_id).first()
    # 开始爬虫此站点
    spider = Spider.Spider(site)
    spider.start_crawl_site(url, deep)


@app.task(ignore_result=True)
def excute_crawl_site_2level_page_task(site_id, site_name, url, deep):
    app.send_task('spider.task.news_crawl.crawl_site_2level_page_task', args=[site_id, site_name, url, deep],
                  queue='crawl_site_2level_page_queue')


if __name__ == '__main__':
    # crawl_site_task(1, '新浪新闻')
    crawl_site_2level_page_task(1, '新浪新闻','http://mil.news.sina.com.cn/',2)
