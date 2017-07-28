# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeChatModel', '0013_auto_20170727_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechatdata',
            name='date_created',
            field=models.DateTimeField(verbose_name='创建时间', default='0'),
        ),
        migrations.AlterField(
            model_name='wechatdata',
            name='date_modified',
            field=models.DateTimeField(verbose_name='更新时间', default='0'),
        ),
    ]
