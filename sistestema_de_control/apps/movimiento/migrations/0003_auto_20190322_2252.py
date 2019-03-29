# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-23 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimiento', '0002_auto_20190315_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingresoproducto',
            name='Nro_de_Compra',
        ),
        migrations.AddField(
            model_name='orden',
            name='Total_paquetes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='Total_sin_descuento',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='descuento',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='ingreso',
            field=models.ManyToManyField(blank=True, null=True, to='movimiento.IngresoProducto'),
        ),
        migrations.AddField(
            model_name='orden',
            name='toto_pago',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
