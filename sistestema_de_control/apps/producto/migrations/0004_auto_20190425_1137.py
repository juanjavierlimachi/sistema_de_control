# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-04-25 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0003_auto_20190321_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='Email',
            field=models.EmailField(blank=True, help_text='Opcional', max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
