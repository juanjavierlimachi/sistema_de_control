# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.views.generic import TemplateView, FormView,ListView,CreateView
from django.core.urlresolvers import reverse_lazy
from .forms import *
from .models import *
# Create your views here.
def inicio(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/logueado/')
	if request.method=='POST':
		formulario=AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario=request.POST['name']
			clave=request.POST['password']
			acceso=authenticate(username=usuario,password=clave)
			if acceso is not None:
				if acceso.is_active and acceso.is_superuser and acceso.is_staff:
					login(request,acceso)
					return HttpResponseRedirect('/logueado/')
				else:
					if acceso.is_active and acceso.is_staff:
						login(request,acceso)
						return HttpResponseRedirect('/logueado/')
					else:
						if acceso.is_active:
							login(request,acceso)
							return HttpResponseRedirect('/logueado/')
			else:
				return render(request,'inicio/login.html',{'mej':'Error, datos incorrectos intente nuevamente gracias.'})
		else:
			return render(request,'inicio/login.html',{'mej':'Error, datos incorrectos intente nuevamente gracias.'})
	else:
		formulario=AuthenticationForm()
	return render(request,'inicio/login.html')
@login_required(login_url='/')
def logueado(request):
	return render(request,'inicio/inicio.html')
@login_required(login_url='/')
def salir(request):
	logout(request)
	return HttpResponseRedirect('/')
class nuevoUser(FormView):
	template_name = 'inicio/nuevoUser.html'
	form_class=UserForm
	success_url = reverse_lazy('listaUsuarios')
	def form_valid(self,form):
		user=form.save()
		perfil=Perfiles()
		perfil.usuario = user
		perfil.ci=form.cleaned_data['ci']
		perfil.telefono=form.cleaned_data['telefono']
		perfil.save()
		return super(nuevoUser, self).form_valid(form)
def DatosUsuario(request):
	users=User.objects.all().order_by("-id")#Mejorar esta consulta
	perfil=Perfiles.objects.all().order_by("-id")
	t_user=Perfiles.objects.all().count()
	return render(request,"inicio/DatosUsuario.html",{'users':users,'perfil':perfil,'t_user':t_user})
def VerUsuario(request,id):
	user=User.objects.get(id=int(id))
	return render(request,'inicio/VerUsuario.html',{'user':user})

def editar_perfil(request):
	if request.method=='POST':
		user_form=UserForms(request.POST,instance=request.user)
		perfil_form=formPerfiles(request.POST,instance=request.user.perfil)
		if user_form.is_valid() and perfil_form.is_valid():
			user_form.save()
			perfil_form.save()
			return HttpResponse("<h2>Actualizaste tus datos correctamente.</h2>")
	else:
		user_form=UserForms(instance=request.user)
		perfil_form=formPerfiles(instance=request.user.perfil)
	return render(request,'inicio/editar_perfil.html',{'user_form':user_form,'perfil_form':perfil_form})

def editarcontracenia(request):
	id_user=request.user
	if request.method=='POST':
		forms=CambioForm(request.POST)
		if forms.is_valid():
			con=request.POST['Nueva_Contracenia']
			fir=request.POST['Confirmacion']
			id_user.set_password(con)
			id_user.save()
			return HttpResponseRedirect('/')
	else:
		forms=CambioForm()
	return render(request,'inicio/editarcontracenia.html',{'forms':forms})
def verificacion(request):
	use=request.GET['use']
	try:
		us=User.objects.get(username=use)
		return HttpResponse("El Nombre de usuario <strong>%s</strong>, ya existe Intente con otro nombre."%(us))
	except User.DoesNotExist:
		return HttpResponse()
@login_required(login_url='/')
def DasactivarUser(request):
	try:
		nombre=request.GET['nombre']
		staff=request.GET['staff']
		user=User.objects.get(username=nombre)
		if staff=='on':
			user.is_active=False
			user.is_staff=False
			user.is_active=False
			user.save()
			return HttpResponse("El Usuario a sido Deshabilitado")
		else:
			return HttpResponse("Haga click en la casilla para Desactivar esta cuenta")
	except User.DoesNotExist:
		return HttpResponse("Haga click en la casilla para Desactivar esta cuenta")
def VolverHavilitar(request):
	try:
		
		nombre=request.GET['nombre']
		user=User.objects.get(username=nombre)
		print user.id
		if request.GET['op']== 'ins':
			user.is_staff=True
			user.is_active=True
			user.is_superuser=False
			user.save()
			return HttpResponse("El Usuario a sido habilitado Personal de almacenes.")
		if request.GET['op']== 'sp':
			user.is_staff=True
			user.is_active=True
			user.is_superuser=True
			user.save()
			return HttpResponse("El Usuario a sido habilitado como Administrador.")
		if request.GET['op'] == 'ca':
			user.is_staff=False
			user.is_active=True
			user.is_superuser=False
			user.save()
			return HttpResponse("El Usuario a sido habilitado como Chofer/ayudante")
		if request.GET['op'] == 'otros':
			user.is_staff=False
			user.is_active=True
			user.is_superuser=False
			user.save()
			return HttpResponse("El Usuario a sido habilitado como personal de la empresa")
		else:
			return HttpResponse("Haga click en la casilla para habilitarlo esta cuenta")
	except User.DoesNotExist:
		return HttpResponse("Haga click en la casilla para habilitarlo esta cuenta")

def  reset_password(request):
	if request.method=='POST':
		forms=FormResetPass(request.POST)
		if forms.is_valid():
			con=request.POST['Nro_Carnet']
			fir=request.POST['Nro_Celular']
			try:
				perfiles = Perfiles.objects.filter(ci=int(con),telefono=int(fir))
				user = 0
				for i in perfiles:

					user = int(i.usuario_id)
					print user
				user = User.objects.get(id=int(user))
				pass_one=request.POST['Nueva_Contracenia']
				pass_tho=request.POST['Confirmacion']
				if pass_one != pass_tho:
					return HttpResponse("<h2> Error su contraseña no coinside, verifique e intente nuevamente gracias.</h2>")
				user.set_password(pass_one)
				
				user.is_staff=False
				user.is_active=True
				user.is_superuser=False
				user.save()
				return HttpResponse("<h2>Cambiaste tu contraseña correctamente, ya puedes ingresar al sistema.</h2>")
			except User.DoesNotExist:
				return HttpResponse("<h2>Error el usuario no existe contactese con el administrador del sistema gracias.</h2>")

			
	else:
		forms=FormResetPass()

	return render(request, 'inicio/reset_password.html',{'forms':forms})






