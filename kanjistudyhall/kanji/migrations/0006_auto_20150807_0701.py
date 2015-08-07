# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanji', '0005_auto_20150807_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kanjicard',
            name='last_missed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='kanjicard',
            name='last_reviewed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='kanjicard',
            name='next_review',
            field=models.DateField(auto_now=True),
        ),
    ]
