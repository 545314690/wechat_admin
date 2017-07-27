# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeChatModel', '0007_auto_20170727_0844'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginuser',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='loginuser',
            name='date_modified',
        ),
        migrations.AddField(
            model_name='wechatdata',
            name='date_created',
            field=models.DateTimeField(default=0, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='wechatdata',
            name='date_modified',
            field=models.DateTimeField(default=0, verbose_name='更新时间'),
        ),
    ]
