from django.http import HttpResponse

from spider.task.workers import app
from spider.task.tasks import add
from spider.task.gather import excute_crawl_history_task
from spider.task.keyword import excute_keyword_task
from spider.task.login import excute_login_task
# 数据库操作
def test_task(request):
    res = app.send_task('spider.task.tasks.add', args=(2, 2), queue='add')
    # res = add(2,2);
    return HttpResponse(res.get(timeout=1))


def gather_history(request):
    excute_crawl_history_task();
    return HttpResponse("开始爬取历史文章...")

def search_keyword(request):
    excute_keyword_task();
    return HttpResponse("开始搜索公众号...")

def login(request):
    excute_login_task();
    return HttpResponse("开始模拟登陆...")
