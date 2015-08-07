# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanji', '0008_auto_20150807_0709'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='kanjicard',
            unique_together=set([('collection', 'kanji'), ('collection', 'mnemonic')]),
        ),
    ]
