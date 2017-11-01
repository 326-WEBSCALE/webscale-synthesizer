# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 23:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synthesizer', '0003_auto_20171031_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippit',
            name='program_spec',
            field=models.TextField(default='Fill me in', help_text='Enter the program spec', max_length=99999),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='snippit',
            name='program_text',
            field=models.TextField(help_text='Enter the program holes', max_length=99999),
        ),
    ]
