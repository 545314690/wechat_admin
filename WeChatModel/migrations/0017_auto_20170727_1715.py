# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeChatModel', '0016_auto_20170727_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wechatdata',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='wechatdata',
            name='date_modified',
        ),
    ]
