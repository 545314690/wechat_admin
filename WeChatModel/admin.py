from django.contrib import admin

# Register your models here.
from django.db.models import Q

from WeChatModel.models import LoginUser, Keyword, WeChatData, WeChatUser


class LoginUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'password', 'enable','date_created','date_modified')  # list
    search_fields = ['name', 'enable']
    list_per_page = 20


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable','crawled','date_created','date_modified')  # list
    search_fields = ['name']
    list_per_page = 20


class WeChatUserAdmin(admin.ModelAdmin):
    list_display = (
        'head_image', 'nickname', 'alias', 'fakeid', 'crawl_history', 'crawled_history', 'monitored', 'enable',
        'description')  # list
    fields = (
        'nickname', 'alias', 'fakeid', ('crawl_history', 'crawled_history', 'monitored', 'enable'),
        'description', 'round_head_img')  # list
    search_fields = ('nickname', 'alias')
    list_per_page = 20


class WeChatDataAdmin(admin.ModelAdmin):
    list_display = (
        'nickname','title', 'pub_time','date_created', 'url')  # list
    search_fields = ('nickname','alias','title','content')
    list_per_page = 10
    ordering = ['date_created','pub_time']
    # inlines = [LoginUserInline]


class LoginUserDao:
    @staticmethod
    def get_enable():
        return LoginUser.objects.filter(enable=True)


class WeChatUserDao:
    # 获取可用并且没有抓取过历史的公众号
    @staticmethod
    def get_enable_and_history_not_crawled():
        return WeChatUser.objects.filter(enable=True, crawled_history=False)

    # 设置为爬取过历史
    @staticmethod
    def set_history_crawled(account):
        return WeChatUser.objects.filter(Q(fakeid=account)).update(crawled_history=True)

    #
    @staticmethod
    def create_by_json(json):
        wechat_user = WeChatUser()
        wechat_user.alias = json.get('alias')
        wechat_user.nickname = json.get('nickname')
        wechat_user.service_type = json.get('service_type')
        wechat_user.round_head_img = json.get('round_head_img')
        wechat_user.fakeid = json.get('fakeid')
        wechat_user.description = ''
        # return WeChatUser.objects.update_or_create(wechat_user)
        return WeChatUser.save(wechat_user)


class KeywordDao:
    # 获取可用关键词
    @staticmethod
    def get_enable():
        return Keyword.objects.filter(enable=True)

    # 获取可用并且没有抓取过的关键词
    @staticmethod
    def get_enable_and_not_crawled():
        return Keyword.objects.filter(enable=True,crawled=False)

    # 设置是否启用
    @staticmethod
    def set_enable(kw, enable):
        return Keyword.objects.filter(Q(name=kw)).update(enable=enable,crawled=True)


admin.site.register(LoginUser, LoginUserAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(WeChatUser, WeChatUserAdmin)
admin.site.register(WeChatData, WeChatDataAdmin)
