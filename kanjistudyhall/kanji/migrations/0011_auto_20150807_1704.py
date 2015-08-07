# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanji', '0010_auto_20150807_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanjicard',
            name='consecutive_correct',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='kanjicard',
            name='last_missed',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='kanjicard',
            name='last_reviewed',
            field=models.DateField(auto_now=True),
        ),
    ]
