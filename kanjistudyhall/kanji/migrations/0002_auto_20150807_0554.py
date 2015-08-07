# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanji', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kanji',
            name='character',
            field=models.CharField(unique=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='kanji',
            name='heisig_index',
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='kanji',
            name='keyword',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
