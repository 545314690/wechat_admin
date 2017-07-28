# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeChatModel', '0005_auto_20170727_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginuser',
            name='date_created',
            field=models.DateTimeField(verbose_name='创建时间', default=None),
        ),
        migrations.AddField(
            model_name='loginuser',
            name='date_modified',
            field=models.DateTimeField(verbose_name='更新时间', default=None),
        ),
    ]
