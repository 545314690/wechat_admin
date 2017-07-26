from django.contrib import admin

# Register your models here.
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline

from WeChatModel.models import LoginUser, Keyword, WeChatData, WeChatUser


class LoginUserInline(GenericStackedInline):
    model = LoginUser


class LoginUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'password', 'enable')  # list
    search_fields = ['name', 'enable']


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable')  # list
    search_fields = ['name']


class WeChatUserAdmin(admin.ModelAdmin):
    list_display = (
        'nickname', 'alias', 'fakeid', 'crawl_history', 'crawled_history', 'monitored', 'enable',
        'description','round_head_img')  # list
    search_fields = ('nickname', 'alias')


class WeChatDataAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'user', 'pub_time', 'url', 'like_num', 'read_num', 'content')  # list
    search_fields = ('nickname', 'alias')
    # inlines = [LoginUserInline]


admin.site.register(LoginUser, LoginUserAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(WeChatUser, WeChatUserAdmin)
admin.site.register(WeChatData, WeChatDataAdmin)
