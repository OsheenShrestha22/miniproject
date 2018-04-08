# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 10:10
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0016_item_is_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=b'', validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='item',
            name='rate',
            field=models.IntegerField(default=b'', validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='item',
            name='total_cost',
            field=models.IntegerField(default=b'', validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)]),
        ),
    ]
