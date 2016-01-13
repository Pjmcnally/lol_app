# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_query', '0003_auto_20160107_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='maststatic',
            name='descript',
            field=models.CharField(max_length=500, default=''),
        ),
    ]
