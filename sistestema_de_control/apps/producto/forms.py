#encoding:utf-8
from django import forms
from django.forms import ModelForm
from .models import *
from .forms import *
from django.contrib.auth.forms import User

opciones = (('Paquete', 'Paquete',), ('Caja', 'Caja',), ('Galones', 'Galones',), ('Otros', 'Otros',))
class FormProducto(ModelForm):
	Unidad=forms.ChoiceField(widget=forms.Select, choices=opciones)
	class Meta:
		model = Producto
		exclude=('Usuario','estado','Stock',)

class FormCategoria(ModelForm):
	class Meta:
		model = Categoria
		exclude=('estado',)

class FormProveedor(ModelForm):
	Telefono = forms.IntegerField(required=True,label='Teléfono')
	Direccion = forms.CharField(required=True ,label='Dirección')
	class Meta():
		model = Proveedor
		exclude=('estado','Usuario',)

