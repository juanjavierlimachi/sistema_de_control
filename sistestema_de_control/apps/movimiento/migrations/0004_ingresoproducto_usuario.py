# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-25 02:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movimiento', '0003_auto_20190322_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingresoproducto',
            name='Usuario',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
