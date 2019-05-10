#encoding:utf-8
from django import forms
from django.forms import ModelForm
from .models import *
from .forms import *
from django.contrib.auth.forms import User
from sistestema_de_control.apps.movimiento.models import *

opciones = (('Paquete', 'Paquete',), ('Caja', 'Caja',), ('Galones', 'Galones',), ('Otros', 'Otros',))
class FormProducto(ModelForm):
	Unidad=forms.ChoiceField(widget=forms.Select, choices=opciones)
	class Meta:
		model = Producto
		exclude=('Usuario','estado','Stock','total',)

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

class FormVehiculo(ModelForm):
	class Meta:
		model = Vehiculo
		exclude=('estado',)

	def __init__(self, *args, **kwargs):
		#seleccionamos todos los usarios que son choferes
		super(FormVehiculo, self).__init__(*args, **kwargs)
		self.fields['Conductor'].queryset = User.objects.filter(is_superuser=False,is_active=True,is_staff=False)

