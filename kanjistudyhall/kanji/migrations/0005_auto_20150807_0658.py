# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanji', '0004_kanjicard_kanji'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kanjicard',
            name='total_reviews',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
