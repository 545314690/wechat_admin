from django import forms
from django.contrib import admin

# Register your models here.

from WeChatModel.models import LoginUser, Keyword, WeChatData, WeChatUser


# 自定义表单
class ImgForm(forms.ModelForm):
    picture = forms.FileField(label='图片', required=False)


# 覆盖 Django admin 代码
def get_form(self, request, obj=None, **kwargs):
    return ImgForm


class LoginUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'password', 'enable')  # list
    search_fields = ['name', 'enable']
    list_per_page = 20


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable')  # list
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
        'title', 'user', 'pub_time', 'url', 'like_num', 'read_num', 'content')  # list
    search_fields = ('title', 'user', 'content')
    list_per_page = 20
    ordering = ['pub_time']
    # inlines = [LoginUserInline]


admin.site.register(LoginUser, LoginUserAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(WeChatUser, WeChatUserAdmin)
admin.site.register(WeChatData, WeChatDataAdmin)