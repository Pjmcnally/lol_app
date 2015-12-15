# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(default='', max_length=500)),
                ('descript', models.CharField(default='', max_length=500)),
                ('image', models.CharField(default='', max_length=500)),
                ('version', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Mastery',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(default='', max_length=500)),
                ('descript', models.CharField(default='', max_length=500)),
                ('tree', models.CharField(default='', max_length=500)),
                ('ranks', models.CharField(default='', max_length=500)),
                ('image', models.CharField(default='', max_length=500)),
                ('version', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Rune',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(default='', max_length=500)),
                ('descript', models.CharField(default='', max_length=500)),
                ('image', models.CharField(default='', max_length=500)),
                ('version', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(default='', max_length=500)),
                ('descript', models.CharField(default='', max_length=500)),
                ('image', models.CharField(default='', max_length=500)),
                ('version', models.CharField(default='', max_length=500)),
            ],
        ),
    ]
