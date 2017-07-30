from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response


# 表单
def index(request):
    return render_to_response('index.html')