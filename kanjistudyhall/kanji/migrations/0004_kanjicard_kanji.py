# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanji', '0003_auto_20150807_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanjicard',
            name='kanji',
            field=models.ForeignKey(to='kanji.Kanji', default=None),
            preserve_default=False,
        ),
    ]
