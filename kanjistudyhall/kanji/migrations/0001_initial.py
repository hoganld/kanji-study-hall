# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kanji',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('character', models.CharField(max_length=1)),
                ('keyword', models.CharField(max_length=50)),
                ('heisig_index', models.PositiveIntegerField()),
            ],
        ),
    ]
