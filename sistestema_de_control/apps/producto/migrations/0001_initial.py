# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-05-24 13:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre_categoria', models.CharField(help_text='Describa la Categoria', max_length=100, unique=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre_producto', models.CharField(max_length=150, unique=True)),
                ('Unidad', models.CharField(max_length=50)),
                ('Precio_compra', models.FloatField(help_text='Ingrese el precio al que compr\xf3')),
                ('Precio_venta', models.FloatField(help_text='Ingrese el precio al que vender\xe1')),
                ('Stock', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('Categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.Categoria')),
                ('Usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre_Razon_Social', models.CharField(max_length=200, unique=True)),
                ('Nit', models.PositiveIntegerField(unique=True)),
                ('Telefono', models.PositiveIntegerField(unique=True)),
                ('Direccion', models.CharField(max_length=150)),
                ('Email', models.EmailField(blank=True, help_text='Opcional', max_length=254, null=True, unique=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
                ('Usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
