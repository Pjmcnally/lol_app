# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_query', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='champion',
            name='key',
            field=models.CharField(max_length=30, default=''),
        ),
        migrations.AddField(
            model_name='champion',
            name='name',
            field=models.CharField(max_length=30, default=''),
        ),
        migrations.AddField(
            model_name='champion',
            name='title',
            field=models.CharField(max_length=100, default=''),
        ),
        migrations.AlterField(
            model_name='champion',
            name='id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
