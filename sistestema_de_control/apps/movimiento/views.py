# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from sistestema_de_control.apps.producto.models import *
from sistestema_de_control.apps.inicio.models import *
from .forms import *
from .models import *
from django.db.models import Q
import datetime
import calendar
from datetime import datetime, date, time, timedelta
from django.db.models import Sum
import StringIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string
# Create your views here.
def ingresa_productos(request,id, ids):
	print "id de la compra",int(ids)
	producto = Producto.objects.get(id=int(id))
	compra=Orden.objects.get(id=int(ids))
	print "el el ids del del proveedor:::",compra.proveedor.id
	if request.method == 'POST':
		trans=IngresoProducto.objects.create(
					cantidad=int(request.POST['cantidad']),
					Precio_unidad=float(request.POST['Precio_unidad']),
					total=float(request.POST['Precio_unidad']) * float(request.POST['cantidad']),
					fecha_de_vencimiento=datetime.strptime(request.POST['fecha_de_vencimiento'],"%d/%m/%Y"),
					producto_id=int(id),
					proveedor_id=int(compra.proveedor.id),
					Usuario_id=int(request.user.id)
				)
		compra.ingreso.add(trans)#ingreso esa transaccion a la compra
		compra.save()#GUARDO LA TRANSACCION
		t_Paquetes = 0
		t_sin_descuento = 0
		descuento = 0
		total_pago = 0

		for i in compra.ingreso.all():
			t_Paquetes = i.cantidad + t_Paquetes
			t_sin_descuento = i.total + t_sin_descuento
			descuento = t_sin_descuento * 0.18
			total_pago = t_sin_descuento - descuento
		Orden.objects.filter(id=int(ids)).update(Total_paquetes=t_Paquetes,Total_sin_descuento=t_sin_descuento,descuento=descuento,toto_pago=total_pago)
		#aki devo agregar todas los ingresos a la compra
		actual=producto.Stock + int(request.POST['cantidad'])
		Producto.objects.filter(id=int(id)).update(Stock=actual)

		return HttpResponse("Registro Exitoso")
	else:
		forms=FormIngreso()
	return render(request,'producto/ingresa_productos.html',{'producto':producto,'forms':forms,'ids':int(ids)})
def verIngresos(request):

	datos 		= IngresoProducto.objects.filter(estado=True).order_by('-id')
	total 		= datos.count()
	proveedores = Proveedor.objects.filter(estado=True).order_by('-id')
	dic =	{
				'datos':datos,
				'total':total,
				'proveedores':proveedores
			}
	return render(request,'movimiento/verIngresos.html',dic)

def ControlStock(request):
	
	return render(request,'movimiento/ControlStock.html',{})

def stock_de_productos(request,id):
	if int(id) == 1:
		datos=Producto.objects.filter(Stock__range=(0,10)).order_by('-id')
	else:
		if int(id) == 2:
			datos=Producto.objects.filter(Stock__range=(11,50)).order_by('-id')
		else:
			if int(id) == 3:
				datos=Producto.objects.filter(Stock__range=(51,10000000)).order_by('-id')
			else:
				if int(id) == 0:
					datos = Producto.objects.all().order_by('-id')
	total = datos.count()
	return render(request,'movimiento/stock_de_productos.html',{'datos':datos,'total':total})

def ImprimiarStock(request, id):
	if int(id) == 1:
		datos=Producto.objects.filter(Stock__range=(0,10)).order_by('-id')
	else:
		if int(id) == 2:
			datos=Producto.objects.filter(Stock__range=(11,50)).order_by('-id')
		else:
			if int(id) == 3:
				datos=Producto.objects.filter(Stock__range=(51,10000000)).order_by('-id')
			else:
				if int(id) == 0:
					datos = Producto.objects.all().order_by('-id')
	total = datos.count()

	html=render_to_string('movimiento/ImprimiarStock.html',{'pagesize':'A4','datos':datos,'total':total})
	return generar_pdf(html)

def generar_pdf(html):
	resultado=StringIO.StringIO()
	pdf=pisa.pisaDocument(StringIO.StringIO(html.encode("UTF:8")),resultado)
	if not pdf.err:
		return HttpResponse(resultado.getvalue(),'application/pdf')
	return HttpResponse("Error al generar el reporte")


def consuta_por_fecha_ingresos(request):
	if request.method == "POST":
		t_paquetes = 0
		t_sin_descuento = 0
		descuento = 0
		total = 0
		
		inicio=datetime.strptime(request.POST['inicio'],"%d/%m/%Y")
		final=datetime.strptime(request.POST['final'],"%d/%m/%Y")
		final = final + timedelta(days=1)
		if int(request.POST['usuario']) == 0 and int(request.POST['user']) == 0:
			#SI ELEJE TODOS LOS USURIO Y TODOS LOS PROVEEDORES
			productos=Orden.objects.filter(fecha_registro__range=(inicio,final),estado=True)

			productos_agrupados = IngresoProducto.objects.filter(fecha_registro__range=(inicio,final)).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'))
			produc = Producto.objects.filter(estado=True)
			for i in productos:
				t_paquetes = t_paquetes + i.Total_paquetes
				t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
				descuento = descuento + i.descuento
				total = total + i.toto_pago

			dat={
				'datos':productos,
				'totalR':productos.count(),
				't_paquetes':t_paquetes,
				't_sin_descuento':t_sin_descuento,
				'descuento':descuento,
				'total':total,
				'inicio':inicio.date(),
				'final':final.date() - timedelta(days=1),
				'productos_agrupados':productos_agrupados,
				'totalPro':productos_agrupados.count(),
				'produc':produc
			}
			return render(request,'movimiento/consuta_por_fecha_ingresos.html',dat)
		else:
			#SI ELEJI TODOS LOS USUARIOS PERO ESCOJE UN PROVEEDOR
			if int(request.POST['usuario']) == 0 and int(request.POST['user']) != 0:
				productos=Orden.objects.filter(proveedor_id=int(request.POST['user']),fecha_registro__range=(inicio,final),estado=True)
				
				productos_agrupados = IngresoProducto.objects.filter(proveedor_id=int(request.POST['user']),fecha_registro__range=(inicio,final)).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'))
				produc = Producto.objects.filter(estado=True)

				proveedor =''
				for i in productos:
					t_paquetes = t_paquetes + i.Total_paquetes
					t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
					descuento = descuento + i.descuento
					total = total + i.toto_pago
					proveedor = i.proveedor

				dat={
					'datos':productos,
					'totalR':productos.count(),
					't_paquetes':t_paquetes,
					't_sin_descuento':t_sin_descuento,
					'descuento':descuento,
					'total':total,
					'inicio':inicio.date(),
					'final':final.date() - timedelta(days=1),
					'proveedor':proveedor,
					'productos_agrupados':productos_agrupados,
					'totalPro':productos_agrupados.count(),
					'produc':produc
				}
				return render(request,'movimiento/consuta_por_fecha_ingresos.html',dat)
			else:
				#SI ELIJE UN USUARIO Y TODOS LOS PROVEEDORES 
				if int(request.POST['user']) == 0 and int(request.POST['usuario']) != 0:
					productos=Orden.objects.filter(Usuario_id=int(request.POST['usuario']),fecha_registro__range=(inicio,final),estado=True)
					productos_agrupados = IngresoProducto.objects.filter(Usuario_id=int(request.POST['usuario']),fecha_registro__range=(inicio,final)).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'))
					produc = Producto.objects.filter(estado=True)


					for i in productos:
						t_paquetes = t_paquetes + i.Total_paquetes
						t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
						descuento = descuento + i.descuento
						total = total + i.toto_pago

					dat={
						'datos':productos,
						'totalR':productos.count(),
						't_paquetes':t_paquetes,
						't_sin_descuento':t_sin_descuento,
						'descuento':descuento,
						'total':total,
						'inicio':inicio.date(),
						'final':final.date() - timedelta(days=1),
						'productos_agrupados':productos_agrupados,
						'totalPro':productos_agrupados.count(),
						'produc':produc
					}
					return render(request,'movimiento/consuta_por_fecha_ingresos.html',dat)
				else:
					#SI ELEJE UN PROVEEDOR Y UN USUARIO
					if int(request.POST['user']) != 0 and int(request.POST['usuario']) != 0:
						productos=Orden.objects.filter(proveedor_id=int(request.POST['user']),Usuario_id=int(request.POST['usuario']),fecha_registro__range=(inicio,final),estado=True)
						
						productos_agrupados = IngresoProducto.objects.filter(proveedor_id=int(request.POST['user']),Usuario_id=int(request.POST['usuario']),fecha_registro__range=(inicio,final)).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'))
						produc = Producto.objects.filter(estado=True)
						for i in productos:
							t_paquetes = t_paquetes + i.Total_paquetes
							t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
							descuento = descuento + i.descuento
							total = total + i.toto_pago

						dat={
							'datos':productos,
							'totalR':productos.count(),
							't_paquetes':t_paquetes,
							't_sin_descuento':t_sin_descuento,
							'descuento':descuento,
							'total':total,
							'inicio':inicio.date(),
							'final':final.date() - timedelta(days=1),
							'productos_agrupados':productos_agrupados,
							'totalPro':productos_agrupados.count(),
							'produc':produc
						}
						return render(request,'movimiento/consuta_por_fecha_ingresos.html',dat)
					else:
						return HttpResponse("Error")
def ReportesIngresos(request, id_user,id_pro,inicio,final):
	if request.method == "GET":
		t_paquetes = 0
		t_sin_descuento = 0
		descuento = 0
		total = 0
		
		inicio=datetime.strptime(inicio,"%d-%m-%Y")
		final=datetime.strptime(final,"%d-%m-%Y")
		final = final + timedelta(days=1)
		if int(id_user) == 0 and int(id_pro) == 0:
			#SI ELEJE TODOS LOS USURIO Y TODOS LOS PROVEEDORES
			productos=Orden.objects.filter(fecha_registro__range=(inicio,final),estado=True)

			productos_agrupados = IngresoProducto.objects.filter(fecha_registro__range=(inicio,final)).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'))
			produc = Producto.objects.filter(estado=True)
			for i in productos:
				t_paquetes = t_paquetes + i.Total_paquetes
				t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
				descuento = descuento + i.descuento
				total = total + i.toto_pago

			dat={
				'pagesize':'later',
				'datos':productos,
				'totalR':productos.count(),
				't_paquetes':t_paquetes,
				't_sin_descuento':t_sin_descuento,
				'descuento':descuento,
				'total':total,
				'inicio':inicio.date(),
				'final':final.date() - timedelta(days=1),
				'productos_agrupados':productos_agrupados,
				'totalPro':productos_agrupados.count(),
				'produc':produc
			}
			html = render_to_string('movimiento/ReportesIngresos.html',dat)
			return generar_pdf(html)
		else:
			#SI ELEJI TODOS LOS USUARIOS PERO ESCOJE UN PROVEEDOR
			if int(id_user) == 0 and int(id_pro) != 0:
				productos=Orden.objects.filter(proveedor_id=int(id_pro),fecha_registro__range=(inicio,final),estado=True)
				
				productos_agrupados = IngresoProducto.objects.filter(proveedor_id=int(id_pro),fecha_registro__range=(inicio,final)).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'))
				produc = Producto.objects.filter(estado=True)

				proveedor =''
				for i in productos:
					t_paquetes = t_paquetes + i.Total_paquetes
					t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
					descuento = descuento + i.descuento
					total = total + i.toto_pago
					proveedor = i.proveedor

				dat={
					'pagesize':'later',
					'datos':productos,
					'totalR':productos.count(),
					't_paquetes':t_paquetes,
					't_sin_descuento':t_sin_descuento,
					'descuento':descuento,
					'total':total,
					'inicio':inicio.date(),
					'final':final.date() - timedelta(days=1),
					'proveedor':proveedor,
					'productos_agrupados':productos_agrupados,
					'totalPro':productos_agrupados.count(),
					'produc':produc
				}
				html = render_to_string('movimiento/ReportesIngresos.html',dat)
				return generar_pdf(html)
			else:
				#SI ELIJE UN USUARIO Y TODOS LOS PROVEEDORES 
				if int(id_user) == 0 and int(id_pro) != 0:
					productos=Orden.objects.filter(Usuario_id=int(id_user),fecha_registro__range=(inicio,final),estado=True)
					productos_agrupados = IngresoProducto.objects.filter(Usuario_id=int(id_user),fecha_registro__range=(inicio,final)).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'))
					produc = Producto.objects.filter(estado=True)


					for i in productos:
						t_paquetes = t_paquetes + i.Total_paquetes
						t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
						descuento = descuento + i.descuento
						total = total + i.toto_pago

					dat={
						'pagesize':'later',
						'datos':productos,
						'totalR':productos.count(),
						't_paquetes':t_paquetes,
						't_sin_descuento':t_sin_descuento,
						'descuento':descuento,
						'total':total,
						'inicio':inicio.date(),
						'final':final.date() - timedelta(days=1),
						'productos_agrupados':productos_agrupados,
						'totalPro':productos_agrupados.count(),
						'produc':produc
					}
					html = render_to_string('movimiento/ReportesIngresos.html',dat)
					return generar_pdf(html)
				else:
					#SI ELEJE UN PROVEEDOR Y UN USUARIO
					if int(id_pro) != 0 and int(id_user) != 0:
						productos=Orden.objects.filter(proveedor_id=int(id_pro),Usuario_id=int(id_user),fecha_registro__range=(inicio,final),estado=True)
						
						productos_agrupados = IngresoProducto.objects.filter(proveedor_id=int(id_pro),Usuario_id=int(id_user),fecha_registro__range=(inicio,final)).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'))
						produc = Producto.objects.filter(estado=True)
						for i in productos:
							t_paquetes = t_paquetes + i.Total_paquetes
							t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
							descuento = descuento + i.descuento
							total = total + i.toto_pago

						dat={
							'pagesize':'later',
							'datos':productos,
							'totalR':productos.count(),
							't_paquetes':t_paquetes,
							't_sin_descuento':t_sin_descuento,
							'descuento':descuento,
							'total':total,
							'inicio':inicio.date(),
							'final':final.date() - timedelta(days=1),
							'productos_agrupados':productos_agrupados,
							'totalPro':productos_agrupados.count(),
							'produc':produc
						}
						html = render_to_string('movimiento/ReportesIngresos.html',dat)
						return generar_pdf(html)
					else:
						return HttpResponse("Error")

			
def NewOrden(request):
	Usuario=Orden(Usuario=request.user)
	if request.method == 'POST':
		forms=FormOrden(request.POST,instance=Usuario)
		if forms.is_valid():
			forms.save()
			ids=Orden.objects.latest('id')
			return HttpResponse(ids.id)
		else:
			HttpResponse("El registro ya existe.")
	else:
		forms=FormOrden(instance=Usuario)
	return render(request,'movimiento/NewOrden.html',{'forms':forms})

def NewOrden_detalle(request, id):
	dato = Orden.objects.get(id=int(id))
	request.session['sesion'] = []#CREO UNA VARIABLE DE SESSION
	detalle = request.session['sesion']
	detalle.append(id)
	request.session['sesion'] = detalle
	# ingresos = IngresoProducto.objects.filter(Nro_de_Compra=int(id),estado=True)
	# total = ingresos.count()
	# costo=0
	# cantidad=0
	# for i in ingresos:
	# 	costo = i.total + costo
	# 	cantidad = i.cantidad + cantidad
	dic={
			'dato':dato
			# 'ingresos':ingresos,
			# 'total':total,
			# 'costo':costo,
			# 'cantidad':cantidad
		}
	return render(request, 'movimiento/NewOrden_detalle.html',dic)


def verConpras(request):
	datos = Orden.objects.all().order_by('-id')
	total = datos.count()
	
	return render(request,'movimiento/verConpras.html',{'datos':datos,'total':total})
def filtar_ingresos(request):
	proveedores = Proveedor.objects.all().order_by('-id')
	user=User.objects.filter(is_superuser=True, is_staff=True, is_active=True)
	return render(request,'movimiento/filtar_ingresos.html',{'proveedores':proveedores,'user':user})
def EditCompra(request,id):
	dato=Orden.objects.get(id=int(id))
	if request.method=='POST':
		forms=FormOrden(request.POST, instance=dato)
		if forms.is_valid():
			forms.save()
			return HttpResponse("El registro se actualizó correctamente.")
	else:
		forms=FormOrden(instance=dato)
	return render(request,'movimiento/EditCompra.html',{'forms':forms,'dato':dato})


from django.db.models import Count

def consuta_ingresos_por_proveedor(request):
	if request.method == "POST":
		inicio=datetime.strptime(request.POST['inicio'],"%d/%m/%Y")
		final=datetime.strptime(request.POST['final'],"%d/%m/%Y")
		print "Proveedores:",int(request.POST['proveedor'])
		final = final + timedelta(days=1)
		if int(request.POST['proveedor']) == 0:
			#SI ELEJE TODOS TODOS LOS PROVEEDORES
			productos=IngresoProducto.objects.filter(fecha_registro__range=(inicio,final),estado=True)
			
			dat={
					'datos':productos,
					'total':productos.count()
				}
			return render(request,'movimiento/consuta_ingresos_por_proveedor.html',dat)
		else:
			productos = IngresoProducto.objects.filter(proveedor_id=int(request.POST['proveedor']),fecha_registro__range=(inicio,final)).values('producto','Precio_unidad').annotate(Total=Sum('cantidad'))
			
			producto = Producto.objects.filter(estado=True)
			for i in productos:
				print "EEEEE",i.values()
				for j in i:
					print "AAAAA",j
			pro=Proveedor.objects.get(id=int(request.POST['proveedor']))
				
			dat = {
					'datos':productos,
					'pro':pro,
					'total':productos.count(),
					'producto':producto
			}
			return render(request,'movimiento/consuta_ingresos_por_proveedor.html',dat)
			
def buscarCompra(request):
	if request.method=="POST":
		texto=request.POST["compra"]
		print "texto",texto
		busqueda=(
			Q(Nro_de_Compra__icontains=texto) |
			Q(Responsable__icontains=texto) |
			Q(id__icontains=texto)
		)
		resultados=Orden.objects.filter(busqueda, estado=True).distinct()
		return render(request,'movimiento/buscarCompra.html',{'resultados':resultados})
	else:
		texto=request.GET["compra"]
		busqueda=(
			Q(Nro_de_Compra__icontains=texto) |
			Q(Responsable__icontains=texto) |
			Q(id__icontains=texto)
		)
		resultados=Orden.objects.filter(busqueda, estado=True).distinct()
		return render(request,'movimiento/buscarCompra.html',{'datos':resultados})

def EditarProductosDeCompra(request, id):
	compra = request.session['sesion']
	ids_deLACompra = compra[0]
	dato=IngresoProducto.objects.get(id=int(id))
	if request.method=='POST':
		IngresoProducto.objects.filter(id=int(id)).update(cantidad=int(request.POST['cantidad']),Precio_unidad=float(request.POST['Precio_unidad']),fecha_de_vencimiento=datetime.strptime(request.POST['fecha_de_vencimiento'],"%d/%m/%Y"),total=float(request.POST['Precio_unidad']) * float(request.POST['cantidad']))
		orden = Orden.objects.get(id=int(ids_deLACompra))
		
		t_Paquetes = 0
		t_sin_descuento = 0
		descuento = 0
		total_pago = 0

		for i in orden.ingreso.all():
			t_Paquetes = i.cantidad + t_Paquetes
			t_sin_descuento = i.total + t_sin_descuento
			descuento = t_sin_descuento * 0.18
			total_pago = t_sin_descuento - descuento
		Orden.objects.filter(id=int(ids_deLACompra)).update(Total_paquetes=t_Paquetes,Total_sin_descuento=t_sin_descuento,descuento=descuento,toto_pago=total_pago)

		return HttpResponse("El registro de actualizó correctamente")
	else:
		forms=FormIngreso(instance=dato)
	return render(request,'movimiento/EditarProductosDeCompra.html',{'forms':forms,'dato':dato,'compra':ids_deLACompra})

def EliminarProductosDeCompra(request,id):
	dato=IngresoProducto.objects.get(id=int(id))
	compra = request.session['sesion']
	ids_deLACompra = compra[0]
	print "Is de la compra",ids_deLACompra
	return render(request,'movimiento/EliminarProductosDeCompra.html',{'dato':dato,'ids_deLACompra':ids_deLACompra})	

def Eliminar_ingreso(request, id):
	dato=IngresoProducto.objects.get(id=int(id))
	compra = request.session['sesion']
	ids_deLACompra = compra[0]
	print "Id de la compra",ids_deLACompra
	ingresos = Orden.objects.get(id=int(ids_deLACompra))
	ingresos.ingreso.remove(id)
	dato.delete()#elimino completamente el dato
	t_Paquetes = 0
	t_sin_descuento = 0
	descuento = 0
	total_pago = 0
	for i in ingresos.ingreso.all():
		t_Paquetes = i.cantidad + t_Paquetes
		t_sin_descuento = i.total + t_sin_descuento
		descuento = t_sin_descuento * 0.18
		total_pago = t_sin_descuento - descuento
	Orden.objects.filter(id=int(ids_deLACompra)).update(Total_paquetes=t_Paquetes,Total_sin_descuento=t_sin_descuento,descuento=descuento,toto_pago=total_pago)
	return HttpResponse("Se eliminó la información correctamente")

def EliminarCompra(request, id):
	dato=Orden.objects.get(id=int(id))
	return render(request,'movimiento/EliminarCompra.html',{'dato':dato})	
def Eliminar_Compra(request, id):
	dato=Orden.objects.get(id=int(id))
	dato.delete()
	return HttpResponse("Se elimino la información correctamente")

