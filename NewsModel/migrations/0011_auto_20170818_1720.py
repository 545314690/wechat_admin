# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-18 09:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsModel', '0010_site_main_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='allow_domains',
            field=models.TextField(blank=True, default=None, verbose_name='允许的域名 正则 '),
        ),
        migrations.AlterField(
            model_name='site',
            name='not_allowed_domains',
            field=models.TextField(blank=True, default=None, verbose_name='不允许的域名 正则 '),
        ),
    ]