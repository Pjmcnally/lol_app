# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_query', '0002_remove_mastery_descript'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Champion',
            new_name='ChampStatic',
        ),
        migrations.RenameModel(
            old_name='Mastery',
            new_name='MastStatic',
        ),
        migrations.RenameModel(
            old_name='Rune',
            new_name='RuneStatic',
        ),
        migrations.RenameModel(
            old_name='Spell',
            new_name='SpellStatic',
        ),
    ]
