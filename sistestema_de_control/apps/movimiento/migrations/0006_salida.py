# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-04-01 19:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movimiento', '0005_auto_20190401_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_salida', models.DateTimeField(auto_now=True)),
                ('Kilometraje', models.PositiveIntegerField(blank=True, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('Movil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movimiento.Vehiculo')),
                ('Usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('salidas', models.ManyToManyField(blank=True, null=True, to='movimiento.SalidaProducto')),
            ],
        ),
    ]
