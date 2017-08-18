from django.http import HttpResponse

from spider.news.SpiderLoader import SpiderLoader


# Create your views here.


def crawl_news_site(request):
    loader = SpiderLoader();
    loader.load_all()
    return HttpResponse("开始爬取新闻站点...")


def crawl_site_by_id(request):
    id = request.GET['id']
    loader = SpiderLoader();
    loader.load_by_id(id)
    return HttpResponse("开始爬取新闻站点: [%s] " % id)
