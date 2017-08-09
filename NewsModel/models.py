from django.db import models

# Create your models here.
from WeChatModel.models import BaseModel


class News(BaseModel):
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    comment_num = models.IntegerField('评论数', default=0)
    url = models.URLField('链接', max_length=255, default=None, unique=True)
    pub_time = models.DateTimeField('发布时间', default=None)
    source = models.CharField('来源', max_length=50, default=None)
    images = models.TextField('图片链接', default=None)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = '新闻'
        verbose_name_plural = '新闻'


class Site(BaseModel):
    enable = models.BooleanField('是否启用', default=True)
    name = models.CharField('站点名', max_length=100, blank=False)
    start_urls = models.TextField('入口页面', blank=False)  # 可多行
    allow_domains = models.TextField('允许的域名 正则 ', default=None)  # 可多行
    url_rule = models.CharField('url 正则 ', default=None, max_length=255)

    title_rule_reg = models.CharField('title 正则 ', default=None, max_length=255, blank=True)
    title_rule_css = models.CharField('title css ', default=None, max_length=255, blank=True)
    title_rule_xpath = models.CharField('title xpath ', default=None, max_length=255, blank=True)

    pub_time_rule_reg = models.CharField('发布时间正则 ', default=None, max_length=255, blank=True)
    pub_time_rule_css = models.CharField('发布时间css ', default=None, max_length=255, blank=True)
    pub_time_rule_xpath = models.CharField('发布时间xpath ', default=None, max_length=255, blank=True)

    source_rule_reg = models.CharField('来源 正则 ', default=None, max_length=255, blank=True)
    source_rule_css = models.CharField('来源 css ', default=None, max_length=255, blank=True)
    source_rule_xpath = models.CharField('来源 xpath ', default=None, max_length=255, blank=True)

    content_rule_reg = models.CharField('内容 正则 ', default=None, max_length=255, blank=True)
    content_rule_css = models.CharField('内容 css ', default=None, max_length=255, blank=True)
    content_rule_xpath = models.CharField('内容 xpath ', default=None, max_length=255, blank=True)

    comment_num_rule_reg = models.CharField('评论数 正则 ', default=None, max_length=255, blank=True)
    comment_num_rule_css = models.CharField('评论数 css ', default=None, max_length=255, blank=True)
    comment_num_rule_xpath = models.CharField('评论数 xpath ', default=None, max_length=255, blank=True)

    images_rule_reg = models.CharField('图片 正则 ', default=None, max_length=255, blank=True)
    images_rule_css = models.CharField('图片 css ', default=None, max_length=255, blank=True)
    images_rule_xpath = models.CharField('图片 xpath ', default=None, max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '新闻站点'
        verbose_name_plural = '新闻站点'