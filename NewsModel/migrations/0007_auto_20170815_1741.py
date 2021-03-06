# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 09:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsModel', '0006_auto_20170815_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='comment_url',
            field=models.URLField(blank=True, default=None, max_length=255, verbose_name='评论URL'),
        ),
        migrations.AlterField(
            model_name='news',
            name='images',
            field=models.TextField(blank=True, default=None, verbose_name='图片链接'),
        ),
        migrations.AlterField(
            model_name='news',
            name='source',
            field=models.CharField(blank=True, default=None, max_length=50, verbose_name='来源'),
        ),
        migrations.AlterField(
            model_name='news',
            name='source_url',
            field=models.URLField(blank=True, default=None, max_length=255, verbose_name='源URL'),
        ),
    ]
