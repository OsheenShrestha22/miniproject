# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 16:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0019_item_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='is_favorite',
        ),
    ]
