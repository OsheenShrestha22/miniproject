# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0022_auto_20171212_2133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generate', models.BooleanField(default=False)),
            ],
        ),
    ]
