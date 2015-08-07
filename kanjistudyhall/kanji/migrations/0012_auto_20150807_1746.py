# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanji', '0011_auto_20150807_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kanjicard',
            name='last_missed',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='kanjicard',
            name='last_reviewed',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='kanjicard',
            name='next_review',
            field=models.DateField(auto_now_add=True),
        ),
    ]
