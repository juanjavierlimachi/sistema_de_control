# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .forms import *
from .models import *
from sistestema_de_control.apps.movimiento.models import *
from django.db.models import Q
import datetime
import calendar
from datetime import datetime, date, time, timedelta
from django.db.models import Sum

# Create your views here.
def NewProducto(request):
	Usuario=Producto(Usuario=request.user)
	if request.method == 'POST':
		forms=FormProducto(request.POST,instance=Usuario)
		if forms.is_valid():
			forms.save()
			return HttpResponse("Registro Exitoso")
	else:
		forms=FormProducto(instance=Usuario)
	return render(request,'producto/NewProducto.html',{'forms':forms})
def EditProducto(request, id):
	dato=Producto.objects.get(id=int(id))
	if request.method=='POST':
		forms=FormProducto(request.POST, instance=dato)
		if forms.is_valid():
			forms.save()
			return HttpResponse("El registro se actualizó correctamente.")
	else:
		forms=FormProducto(instance=dato)
	return render(request,'producto/EditProducto.html',{'forms':forms,'dato':dato})

def verProducto(request):
	datos = Producto.objects.all().order_by('-id')
	total = datos.count()
	return render(request,'producto/verProducto.html',{'datos':datos,'total':total})
def verCategorias(request):
	datos = Categoria.objects.all().order_by('-id')
	total = Categoria.objects.all().count()
	return render(request,'producto/verCategorias.html',{'datos':datos,'total':total})
def NewCategoria(request):
	if request.method == 'POST':
		forms=FormCategoria(request.POST)
		if forms.is_valid():
			forms.save()
			return HttpResponse("Registro Exitoso")
	else:
		forms=FormCategoria()
	return render(request,'producto/NewCategoria.html',{'forms':forms})

def kardexProducto(request,id):
	dato=Producto.objects.get(id=int(id))
	valor = float(dato.Precio_compra) * float(dato.Stock)

	fecha=datetime.now()
	inicio="%s-%s-01" % (fecha.year, fecha.month)
	final="%s-%s-%s" % (fecha.year, fecha.month, calendar.monthrange(fecha.year-1, fecha.month+1)[1])


	Total_ingresos=IngresoProducto.objects.filter(producto_id=int(id),fecha_registro__range=(inicio,final))
	
	#Total_ingresos=IngresoProducto.objects.filter(producto=int(id)).count()
	bsi = 0
	for i in Total_ingresos:
		bsi  = float(i.total) + float(bsi)

	dic={'dato':dato,'valor':valor,'Total_ingresos':Total_ingresos.count(),'bsi':bsi}
	return render(request,'producto/kardexProducto.html',dic)

def VerProveedores(request):
	datos = Proveedor.objects.all().order_by('-id')
	total = Proveedor.objects.all().count()
	return render(request,'producto/VerProveedores.html',{'datos':datos,'total':total})
def NewProveedor(request):
	Usuario=Proveedor(Usuario=request.user)
	if request.method == 'POST':
		forms=FormProveedor(request.POST,instance=Usuario)
		if forms.is_valid():
			forms.save()
			return HttpResponse("Registro Exitoso...!")
	else:
		forms=FormProveedor(instance=Usuario)
	return render(request,'producto/NewProveedor.html',{'forms':forms})
def EditarProveedor(request, id):
	dato=Proveedor.objects.get(id=int(id))
	if request.method=='POST':
		forms=FormProveedor(request.POST, instance=dato)
		if forms.is_valid():
			forms.save()
			return HttpResponse("El registro se actualizó correctamente.")
	else:
		forms=FormProveedor(instance=dato)
	return render(request,'producto/EditarProveedor.html',{'forms':forms,'dato':dato})
def EliminarProveedor(request, id):
	dato=Proveedor.objects.get(id=int(id))
	return render(request,'producto/EliminarProveedor.html',{'dato':dato})	
def Eliminar_Proveedor(request, id):
	dato=Proveedor.objects.get(id=int(id))
	Proveedor.objects.filter(id=int(id)).update(estado=False)
	return HttpResponse("Se dió de baja la información:   %s"%(dato.Nombre_Razon_Social))
def AltaProveedor(request, id):
	dato=Proveedor.objects.get(id=int(id))
	return render(request,'producto/AltaProveedor.html',{'dato':dato})
	
def recuperarProveedor(request, id):
	dato=Proveedor.objects.get(id=int(id))
	Proveedor.objects.filter(id=int(id)).update(estado=True)
	return HttpResponse("Se recuperó la información:   %s  correctamente"%(dato.Nombre_Razon_Social))

def buscar_producto(request):
	ids = request.GET['ids']
	return render(request,'producto/buscar_producto.html',{'ids':int(ids)})

def buscarProducto(request,id):
	ids = int(id)
	if request.method=="POST":
		texto=request.POST["producto"]
		busqueda=(
			Q(Nombre_producto__icontains=texto) |
			Q(Nombre_producto__icontains=texto) |
			Q(id__icontains=texto)
		)
		resultados=Producto.objects.filter(busqueda, estado=True).distinct()
		return render(request,'producto/buscarProducto.html',{'resultados':resultados,'ids':ids})
	else:
		texto=request.GET["producto"]
		busqueda=(
			Q(Nombre_producto__icontains=texto) |
			Q(Nombre_producto__icontains=texto) |
			Q(id__icontains=texto)
		)
		resultados=Producto.objects.filter(busqueda, estado=True).distinct()
		return render(request,'producto/buscarProducto.html',{'resultados':resultados,'ids':ids})
def EditCategorias(request, id):
	dato=Categoria.objects.get(id=int(id))
	if request.method=='POST':
		forms=FormCategoria(request.POST, instance=dato)
		if forms.is_valid():
			forms.save()
			return HttpResponse("El registro se actualizó correctamente.")
	else:
		forms=FormCategoria(instance=dato)
	return render(request,'producto/EditCategorias.html',{'forms':forms,'dato':dato})
def EliminarCategorias(request, id):
	dato=Categoria.objects.get(id=int(id))
	return render(request,'producto/EliminarCategorias.html',{'dato':dato})	
def Eliminar_Categoria(request, id):
	dato=Categoria.objects.get(id=int(id))
	Categoria.objects.filter(id=int(id)).update(estado=False)
	return HttpResponse("Se dió de baja la información:   %s"%(dato.Nombre_categoria))

def dar_baja_producto(request, id):
	dato=Producto.objects.get(id=int(id))
	return render(request,'producto/dar_baja_producto.html',{'dato':dato})	
def Eliminar_producto(request, id):
	dato=Producto.objects.get(id=int(id))
	Producto.objects.filter(id=int(id)).update(estado=False)
	return HttpResponse("Se dió de baja la información:   %s"%(dato.Nombre_producto))

def dar_altaProducto(request, id):
	dato=Producto.objects.get(id=int(id))
	return render(request,'producto/dar_altaProducto.html',{'dato':dato})	

def recuperarProducto(request, id):
	dato=Producto.objects.get(id=int(id))
	Producto.objects.filter(id=int(id)).update(estado=True)
	return HttpResponse("Se recuperó la información:   %s  correctamente"%(dato.Nombre_producto))	
def AltaCategorias(request, id):
	dato=Categoria.objects.get(id=int(id))
	return render(request,'producto/AltaCategoria.html',{'dato':dato})
def recuperarCategoria(request, id):
	dato=Categoria.objects.get(id=int(id))
	Categoria.objects.filter(id=int(id)).update(estado=True)
	return HttpResponse("Se recuperó la información:   %s  correctamente"%(dato.Nombre_categoria))

