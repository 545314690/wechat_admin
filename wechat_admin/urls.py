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

import testdb
from spider.controller.spider_controller import gather_history, search_keyword
from spider.controller.spider_controller import test_task

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test_save_user$', testdb.test_save_user),
    url(r'^test_get_user$', testdb.test_get_user),
    url(r'^test_update$', testdb.test_update),
    url(r'^test_remove$', testdb.test_remove),
    url(r'^test_task', test_task),
    url(r'^gather_history', gather_history),
    url(r'^search_keyword', search_keyword),
]
