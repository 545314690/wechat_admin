# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('WeChatModel', '0011_auto_20170727_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechatdata',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 27, 9, 11, 11, 189249, tzinfo=utc), verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='wechatdata',
            name='date_modified',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 27, 9, 11, 11, 189274, tzinfo=utc), verbose_name='更新时间'),
        ),
    ]
