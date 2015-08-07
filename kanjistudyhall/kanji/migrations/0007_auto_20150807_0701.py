# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanji', '0006_auto_20150807_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kanjicard',
            name='efactor',
            field=models.FloatField(default=2.5),
        ),
    ]
