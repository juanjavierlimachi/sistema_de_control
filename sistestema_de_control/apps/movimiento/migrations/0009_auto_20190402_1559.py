# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-04-02 19:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimiento', '0008_auto_20190401_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='Placa',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
