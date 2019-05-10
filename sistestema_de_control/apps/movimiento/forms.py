#encoding:utf-8
from django import forms
from django.forms import ModelForm
from .models import *
from .forms import *
from django.contrib.auth.forms import User

#opciones = (('NO', 'NO',), ('SI', 'SI',))
class FormIngreso(ModelForm):
	class Meta:
		model = IngresoProducto
		exclude=('estado','Usuario','Precio_unidad','total','producto','Nro_de_Compra','proveedor',)
class FormOrden(ModelForm):
	class Meta:
		model = Orden
		exclude=('estado','Usuario','Total_paquetes','Total_sin_descuento','descuento','toto_pago','ingreso',)

class FormSalida(ModelForm):
	class Meta:
		model = Salida
		exclude=('estado','Usuario','Total','Metas','Avanse','Porsentaje','Total_a_pagar','salidas',)


class FormSalidaMovil(ModelForm):
	class Meta:
		model = SalidaProducto
		exclude=('estado','Usuario','Precio_venta','total','producto','Movil',)
		