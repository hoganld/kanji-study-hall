# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kanji', '0002_auto_20150807_0554'),
    ]

    operations = [
        migrations.CreateModel(
            name='KanjiCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('mnemonic', models.TextField()),
                ('total_reviews', models.PositiveIntegerField()),
                ('last_reviewed', models.DateTimeField()),
                ('last_missed', models.DateTimeField()),
                ('next_review', models.DateField()),
                ('efactor', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='KanjiCardCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='kanjicard',
            name='collection',
            field=models.ForeignKey(to='kanji.KanjiCardCollection'),
        ),
    ]
