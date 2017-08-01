from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response

from spider.task.gather import excute_crawl_history_task
from spider.task.keyword import excute_keyword_task
from spider.task.login import excute_login_task

# 表单
from spider.task.workers import app


def index(request):
    return render_to_response('index.html')

# 数据库操作
def test_task(request):
    res = app.send_task('spider.task.tasks.add', args=(2, 0), queue='add')
    # res = add(2,2);
    return HttpResponse("ssssss")
    # return HttpResponse(res.get(timeout=1))


def gather_history(request):
    excute_crawl_history_task();
    return HttpResponse("开始爬取历史文章...")

def search_keyword(request):
    excute_keyword_task();
    return HttpResponse("开始搜索公众号...")

def login(request):
    excute_login_task();
    return HttpResponse("开始模拟登陆...")