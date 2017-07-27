from django.http import HttpResponse

from .tasks import add


# 数据库操作
def test_task(request):
    res = add.apply_async((2, 2), queue='add')
    return HttpResponse(res.get(timeout=1))
