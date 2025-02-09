# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=250)),
                ('product_name', models.CharField(max_length=250)),
                ('quantity', models.IntegerField(max_length=100)),
                ('rate', models.IntegerField(max_length=100)),
                ('total_cost', models.IntegerField(max_length=100)),
                ('product_logo', models.CharField(max_length=1000)),
            ],
        ),
    ]
