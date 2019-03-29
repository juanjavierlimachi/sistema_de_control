#encoding:utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *
from .forms import *
from django.contrib.auth.forms import User
class UserForm(UserCreationForm):
	username = forms.CharField(max_length=40,help_text="Nombre de usuario (No deve contener espacios) *")
	password1 = forms.CharField(help_text="Recuerde este dato para proporcionar al personal *")
	password2 = forms.CharField(help_text="Confirme la contraseña anterior *")
	first_name = forms.CharField(max_length=140, label="Nombre y Apellido *")
	#email = forms.EmailField(label='Correo Elec.')
	ci = forms.IntegerField(label="Nro. de Carnet. *")
	telefono = forms.IntegerField(label="Teléfono/Celular *")
	def clean_ci(self):
		ci=self.cleaned_data['ci']
		if len(str(ci))>11 or len(str(ci))<=5:
			raise forms.ValidationError('El Nro. de CI. deve ser 6 a 10 dígitos')
		try:
			p=Perfiles.objects.get(ci=ci)
		except Perfiles.DoesNotExist:
			return ci
		raise forms.ValidationError('El Nro. de CI. ya Existe')
	def clean_telefono(self):
		telefono=self.cleaned_data['telefono']
		if len(str(telefono))>9 or len(str(telefono))<=7:
			raise forms.ValidationError('El Nro. de Teléfono deve ser 8 dígitos')
		try:
			p = Perfiles.objects.get(telefono=telefono)
		except Perfiles.DoesNotExist:
			return telefono
		raise forms.ValidationError('El Numero de teléfono ya existe')
	class Meta:
		model=User
		fields=("username","password1","password2","first_name","ci","telefono")
		widgets = {
			'password1':forms.PasswordInput(),
		}
	def save(self,commit=True):
		user=super(UserForm,self).save(commit=False)
		user.first_name=self.cleaned_data.get("first_name")
		if commit:
			user.is_active = False
			user.is_staff = False
			user.is_superuser = False
			user.save()
		return user
class formPerfiles(forms.ModelForm):
	class Meta:
		model=Perfiles
		exclude=['usuario']
class UserForms(forms.ModelForm):
	class Meta:
		model=User
		fields = ('username','first_name')

class CambioForm(forms.Form):
	Nueva_Contracenia= forms.CharField(required=True, label="Contraseña",widget=forms.PasswordInput(render_value=False))
	Confirmacion	 = forms.CharField(required=True, label="Confirmar",widget=forms.PasswordInput(render_value=False))
	def password(self):
		pass_one=self.cleaned_data['Nueva_Contracenia']
		pass_tho=self.cleaned_data['Confirmacion']
		if pass_one == pass_tho:
			pass
		else:
			raise forms.ValidationError('Error: Los datos no Coinsiden')
class FormResetPass(forms.Form):
	Nro_Carnet= forms.IntegerField(required=True, label="Ingrese su número de Carnet")
	Nro_Celular= forms.IntegerField(required=True, label="Ingrese su número de Celular ó teléfono")
	
	Nueva_Contracenia = forms.CharField(required=True, label="Escriba su nueva contraseña",widget=forms.PasswordInput(render_value=False))
	Confirmacion = forms.CharField(required=True, label="Confirme nuevamente",widget=forms.PasswordInput(render_value=False))
	def password(self):
		pass_one=self.cleaned_data['Nueva_Contracenia']
		pass_tho=self.cleaned_data['Confirmacion']
		if pass_one == pass_tho:
			pass
		else:
			raise forms.ValidationError('Error: Los datos no Coinsiden')