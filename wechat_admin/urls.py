"""wechat_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from WeChatModel.views import test_task, index, gather_history, search_keyword, login
from NewsModel.views import crawl_news_site, crawl_site_by_id

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test_task', test_task),
    url(r'^gather_history', gather_history),
    url(r'^search_keyword', search_keyword),
    url(r'^news/crawl_news_site', crawl_news_site),
    url(r'^news/crawl_site_by_id', crawl_site_by_id),
    url(r'^login', login),
    url(r'^index', index),
]
