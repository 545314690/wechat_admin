from django.contrib import admin

# Register your models here.
from NewsModel.models import News, Site


class NewsAdmin(admin.ModelAdmin):
    list_display = (
        'source', 'title', 'pub_time', 'comment_num', 'url')  # list
    search_fields = ('title', 'source', 'url')
    list_per_page = 10


class SiteAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'enable', 'start_urls', 'allow_domains', 'url_rule',
        'title_rule_css', 'title_rule_xpath', 'title_rule_reg',
        'pub_time_rule_css', 'pub_time_rule_xpath', 'pub_time_rule_reg',
        'source_rule_css', 'source_rule_xpath', 'source_rule_reg',
        'content_rule_css', 'content_rule_xpath', 'content_rule_reg',
        'comment_num_rule_css', 'comment_num_rule_xpath', 'comment_num_rule_reg',
        'images_rule_css', 'images_rule_xpath', 'images_rule_reg',
    )  # list
    search_fields = ('name', 'allow_domains')
    fields = (
        'name', 'enable', 'start_urls', 'allow_domains', 'url_rule',
        ('title_rule_css', 'title_rule_xpath', 'title_rule_reg'),
        ('pub_time_rule_css', 'pub_time_rule_xpath', 'pub_time_rule_reg'),
        ('source_rule_css', 'source_rule_xpath', 'source_rule_reg'),
        ('content_rule_css', 'content_rule_xpath', 'content_rule_reg'),
        ('comment_num_rule_css', 'comment_num_rule_xpath', 'comment_num_rule_reg'),
        ('images_rule_css', 'images_rule_xpath', 'images_rule_reg'),
    )
    list_per_page = 10


admin.site.register(News, NewsAdmin)
admin.site.register(Site, SiteAdmin)
