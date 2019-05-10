# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.forms import User
# Create your models here.
class Categoria(models.Model):
	Nombre_categoria=models.CharField(max_length=100, unique=True,help_text="Describa la Categoria")
	fecha_registro = models.DateTimeField(auto_now_add=True)
	estado=models.BooleanField(default=True)
	def __unicode__(self):
		return self.Nombre_categoria
class Producto(models.Model):
	Nombre_producto=models.CharField(max_length=150, unique=True)
	Unidad=models.CharField(max_length=50)
	Precio_compra=models.FloatField()#precio de compra
	Precio_venta=models.FloatField()#precio de venta
	Stock=models.IntegerField(default=0)
	total=models.IntegerField(default=0)
	Usuario=models.ForeignKey(User)
	Categoria=models.ForeignKey(Categoria)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	estado=models.BooleanField(default=True)
	def __unicode__(self):
		return self.Nombre_producto
class Proveedor(models.Model):
	Nombre_Razon_Social=models.CharField(max_length=200, unique=True)
	Nit=models.PositiveIntegerField(unique=True)
	Telefono=models.PositiveIntegerField(unique=True)
	Direccion=models.CharField(max_length=150)
	Email=models.EmailField(unique=True, blank=True, null=True, help_text="Opcional")
	fecha_registro = models.DateTimeField(auto_now_add=True)
	estado=models.BooleanField(default=True)
	Usuario=models.ForeignKey(User)
	def __unicode__(self):
		return self.Nombre_Razon_Social