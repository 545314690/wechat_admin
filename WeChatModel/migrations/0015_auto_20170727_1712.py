# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeChatModel', '0014_auto_20170727_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechatdata',
            name='date_created',
            field=models.DateTimeField(verbose_name='创建时间', default='0000-00-00 00:00:00'),
        ),
        migrations.AlterField(
            model_name='wechatdata',
            name='date_modified',
            field=models.DateTimeField(verbose_name='更新时间', default='0000-00-00 00:00:00'),
        ),
    ]
