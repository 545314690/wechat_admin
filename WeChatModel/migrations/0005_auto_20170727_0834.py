# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeChatModel', '0004_auto_20170725_2328'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keyword',
            options={'verbose_name_plural': '关键词', 'verbose_name': '关键词'},
        ),
        migrations.AlterModelOptions(
            name='loginuser',
            options={'verbose_name_plural': '登录用户', 'verbose_name': '登录用户'},
        ),
        migrations.AlterModelOptions(
            name='wechatdata',
            options={'verbose_name_plural': '微信文章', 'verbose_name': '微信文章'},
        ),
        migrations.AlterModelOptions(
            name='wechatuser',
            options={'verbose_name_plural': '微信公众号', 'verbose_name': '微信公众号'},
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='alias',
            field=models.CharField(max_length=100, verbose_name='别名'),
        ),
        migrations.AlterField(
            model_name='wechatuser',
            name='fakeid',
            field=models.CharField(max_length=100, default=None, unique=True, verbose_name='biz'),
        ),
    ]
