# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 13:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_remove_transaction_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='rate',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='total_cost',
        ),
    ]
