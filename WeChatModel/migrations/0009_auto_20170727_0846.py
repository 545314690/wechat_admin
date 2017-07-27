# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('WeChatModel', '0008_auto_20170727_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechatdata',
            name='date_created',
            field=models.DateTimeField(verbose_name='创建时间', default=datetime.datetime(2017, 7, 27, 8, 46, 56, 735623, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='wechatdata',
            name='date_modified',
            field=models.DateTimeField(verbose_name='更新时间', default=datetime.datetime(2017, 7, 27, 8, 46, 56, 735651, tzinfo=utc)),
        ),
    ]
