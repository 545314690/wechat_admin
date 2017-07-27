from django.http import HttpResponse

from .tasks import add


# 数据库操作
def test_task(request):
    res = add.delay(2, 2)
    return HttpResponse(res.get(timeout=1))
