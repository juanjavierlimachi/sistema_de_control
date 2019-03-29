# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sistestema_de_control.apps.producto.models import *

from django.contrib.auth.forms import User
from django.db import models

# Create your models here.
class IngresoProducto(models.Model):
	cantidad=models.PositiveIntegerField()
	Precio_unidad=models.FloatField()
	total=models.FloatField()
	fecha_de_vencimiento=models.DateField()
	producto=models.ForeignKey(Producto)
	proveedor=models.ForeignKey(Proveedor)
	Usuario=models.ForeignKey(User)
	fecha_registro=models.DateTimeField(auto_now=True)
	estado=models.BooleanField(default=True)
	def __unicode__(self):
		return "%s, %s"%(self.fecha_de_vencimiento,self.producto)

class Orden(models.Model):
	Nro_de_Compra = models.PositiveIntegerField(unique=True)
	Responsable = models.CharField(max_length=150)
	Cortesia = models.TextField(blank=True, null=True, help_text="Describa las cortesias que se ingreso.")
	Usuario=models.ForeignKey(User)
	proveedor=models.ForeignKey(Proveedor)

	Total_paquetes = models.IntegerField(blank=True, null=True)
	Total_sin_descuento = models.FloatField(blank=True, null=True)
	descuento = models.FloatField(blank=True, null=True)
	toto_pago = models.FloatField(blank=True, null=True)
	ingreso = models.ManyToManyField(IngresoProducto, blank=True, null=True)

	fecha_registro=models.DateTimeField(auto_now=True)
	estado=models.BooleanField(default=True)
	def __unicode__(self):
		return "%s"%(self.Nro_de_Compra)

