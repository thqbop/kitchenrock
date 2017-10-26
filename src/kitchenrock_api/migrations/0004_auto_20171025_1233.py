# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-10-25 12:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kitchenrock_api', '0003_auto_20171020_1156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodrecipe',
            name='categories',
        ),
        migrations.AddField(
            model_name='foodrecipe',
            name='categories',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='kitchenrock_api.FoodCategory'),
            preserve_default=False,
        ),
    ]