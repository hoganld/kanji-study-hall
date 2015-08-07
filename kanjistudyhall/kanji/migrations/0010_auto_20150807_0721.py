# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanji', '0009_auto_20150807_0712'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='kanjicardcollection',
            unique_together=set([('owner', 'name')]),
        ),
    ]
