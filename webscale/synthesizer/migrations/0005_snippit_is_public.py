# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synthesizer', '0004_auto_20171101_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippit',
            name='is_public',
            field=models.BooleanField(default=True, help_text="Toggle for user's public visibility"),
        ),
    ]
