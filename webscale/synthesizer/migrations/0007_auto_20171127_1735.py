# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-27 22:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('synthesizer', '0006_googleauth_is_authenticated'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='OldUser',
        ),
    ]