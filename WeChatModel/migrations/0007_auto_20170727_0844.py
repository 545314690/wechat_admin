# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeChatModel', '0006_auto_20170727_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginuser',
            name='date_created',
            field=models.DateTimeField(default=0, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='loginuser',
            name='date_modified',
            field=models.DateTimeField(default=0, verbose_name='更新时间'),
        ),
    ]
