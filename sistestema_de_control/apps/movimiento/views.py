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
					Precio_unidad=float(producto.Precio_compra),
					total=float(producto.Precio_compra) * float(request.POST['cantidad']),
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
		Imvercion_Producto = int(producto.Precio_compra) * int(actual)
		Producto.objects.filter(id=int(id)).update(Stock=actual,total=Imvercion_Producto)

		return HttpResponse("Registro Exitoso")
	else:
		forms=FormIngreso()
	return render(request,'producto/ingresa_productos.html',{'producto':producto,'forms':forms,'ids':int(ids)})

def salida_productos(request, id, ids):
	print "id de la salida",int(ids)
	producto = Producto.objects.get(id=int(id))
	compra=Salida.objects.get(id=int(ids))#hago una consulta al modelo Salida

	if request.method == 'POST':
		if producto.Stock <= 0 or int(request.POST['cantidad']) > producto.Stock:
			return HttpResponse("NO SE REGISTRÓ LA SALIDA PORQUE LOS DATOS NO SON VÁLDOS, INTENTE NUEVAMENTE GRACIAS.")
		else:
			trans=SalidaProducto.objects.create(
						cantidad=int(request.POST['cantidad']),
						Precio_venta=float(producto.Precio_venta),
						total=float(producto.Precio_venta) * float(request.POST['cantidad']),
						producto_id=int(id),
						Movil_id=int(compra.Movil.id),
						Usuario_id=int(request.user.id)
					)
			compra.salidas.add(trans)#ingreso esa transaccion a la compra
			compra.save()#GUARDO LA TRANSACCION
			t_Paquetes = 0
			Metas = 0
			Avanse = 0
			Porsentaje = 0
			total_pago = 0

			for i in compra.salidas.all():
				t_Paquetes = i.cantidad + t_Paquetes
				# t_sin_descuento = i.total + t_sin_descuento
				# descuento = t_sin_descuento * 0.18
				total_pago = i.total + total_pago
			Salida.objects.filter(id=int(ids)).update(Total=t_Paquetes,Total_a_pagar=total_pago)
			#aki devo agregar todas los ingresos a la compra
			actual=producto.Stock - int(request.POST['cantidad'])
			Imvercion_Producto = int(producto.Precio_compra) * int(actual)
			Producto.objects.filter(id=int(id)).update(Stock=actual,total=Imvercion_Producto)

			return HttpResponse("Registro Exitoso")
	else:
		forms=FormSalidaMovil()
	return render(request,'producto/salida_productos.html',{'producto':producto,'forms':forms,'ids':int(ids)})

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
		datos=Producto.objects.filter(Stock__range=(0,10),estado=True).order_by('-id')
	else:
		if int(id) == 2:
			datos=Producto.objects.filter(Stock__range=(11,50),estado=True).order_by('-id')
		else:
			if int(id) == 3:
				datos=Producto.objects.filter(Stock__range=(51,10000000),estado=True).order_by('-id')
			else:
				if int(id) == 0:
					datos = Producto.objects.filter(estado=True).order_by('-id')
				else:
					if int(id) == 4:
						datos = Producto.objects.filter(estado=False).order_by('-id')
	print datos.count()
	t_compras = 0
	t_ventas = 0
	t = 0
	stock = 0
	for i in datos:
		t_ventas = (i.Stock * i.Precio_venta) + t_ventas
		t_compras = (i.Stock * i.Precio_compra) + t_compras
		t = i.total + t
		stock = i.Stock + stock
	return render(request,'movimiento/stock_de_productos.html',{'datos':datos,'t_ventas':t_ventas,'t_compras':t_compras,'t':t,'stock':stock})

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
					datos = Producto.objects.filter(estado=True).order_by('-id')
				else:
					if int(id) == 4:
						datos = Producto.objects.filter(estado=False).order_by('-id')
	total = datos.count()

	html=render_to_string('movimiento/ImprimiarStock.html',{'pagesize':'A4','datos':datos,'total':total,'ids':id})
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
def consuta_por_fecha_salidas(request):
	if request.method == "POST":
		t_paquetes = 0
		t_sin_descuento = 0
		descuento = 0
		total = 0
		inicio=datetime.strptime(request.POST['inicio'],"%d/%m/%Y")
		final=datetime.strptime(request.POST['final'],"%d/%m/%Y")
		final = final + timedelta(days=1)
		#user  Vehiculos
		if int(request.POST['usuario']) == 0 and int(request.POST['user']) == 0:
			#SI ELEJE TODOS LOS USURIO Y TODOS LOS PROVEEDORES
			productos=Salida.objects.filter(fecha_salida__range=(inicio,final),estado=True)

			productos_agrupados = SalidaProducto.objects.filter(fecha_registro__range=(inicio,final)).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'))
			produc = Producto.objects.filter(estado=True)
			# for i in productos:
			# 	t_paquetes = t_paquetes + i.Total_paquetes
			# 	t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
			# 	descuento = descuento + i.descuento
			# 	total = total + i.toto_pago

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
			return render(request,'movimiento/consuta_por_fecha_salidas.html',dat)
		else:
			#SI ELEJI TODOS LOS USUARIOS PERO ESCOJE UN PROVEEDOR
			if int(request.POST['usuario']) == 0 and int(request.POST['user']) != 0:
				productos=Salida.objects.filter(Movil_id=int(request.POST['user']),fecha_salida__range=(inicio,final),estado=True)
				
				productos_agrupados = SalidaProducto.objects.filter(Movil_id=int(request.POST['user']),fecha_salida__range=(inicio,final)).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('Total_a_pagar'))
				produc = Producto.objects.filter(estado=True)

				proveedor =''
				for i in productos:
					# t_paquetes = t_paquetes + i.Total_paquetes
					# t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
					# descuento = descuento + i.descuento
					# total = total + i.toto_pago
					proveedor = i.Movil

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
				return render(request,'movimiento/consuta_por_fecha_salidas.html',dat)
			else:
				#SI ELIJE UN USUARIO Y TODOS LOS PROVEEDORES 
				if int(request.POST['user']) == 0 and int(request.POST['usuario']) != 0:
					productos=Salida.objects.filter(Usuario_id=int(request.POST['usuario']),fecha_salida__range=(inicio,final),estado=True)
					productos_agrupados = SalidaProducto.objects.filter(Usuario_id=int(request.POST['usuario']),fecha_salida__range=(inicio,final)).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('Total_a_pagar'))
					produc = Producto.objects.filter(estado=True)


					# for i in productos:
					# 	t_paquetes = t_paquetes + i.Total_paquetes
					# 	t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
					# 	descuento = descuento + i.descuento
					# 	total = total + i.toto_pago

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
					return render(request,'movimiento/consuta_por_fecha_salidas.html',dat)
				else:
					#SI ELEJE UN PROVEEDOR Y UN USUARIO
					if int(request.POST['user']) != 0 and int(request.POST['usuario']) != 0:
						productos=Orden.objects.filter(Movil_id=int(request.POST['user']),Usuario_id=int(request.POST['usuario']),fecha_salida__range=(inicio,final),estado=True)
						
						productos_agrupados = IngresoProducto.objects.filter(Movil_id=int(request.POST['user']),Usuario_id=int(request.POST['usuario']),fecha_salida__range=(inicio,final)).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('Total_a_pagar'))
						produc = Producto.objects.filter(estado=True)
						# for i in productos:
						# 	t_paquetes = t_paquetes + i.Total_paquetes
						# 	t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
						# 	descuento = descuento + i.descuento
						# 	total = total + i.toto_pago

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
						return render(request,'movimiento/consuta_por_fecha_salidas.html',dat)
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
						proveedor =''
						usuario=''
						for i in productos:
							t_paquetes = t_paquetes + i.Total_paquetes
							t_sin_descuento = t_sin_descuento + i.Total_sin_descuento
							descuento = descuento + i.descuento
							total = total + i.toto_pago
							proveedor = i.proveedor
							usuario = i.Usuario

						dat={
							'pagesize':'later',
							'datos':productos,
							'totalR':productos.count(),
							't_paquetes':t_paquetes,
							't_sin_descuento':t_sin_descuento,
							'descuento':descuento,
							'total':total,
							'proveedor':proveedor,
							'usuario':usuario,
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

def ReportesSalidas(request, id_user,id_movil,inicio,final):
	
	return HttpResponse("EN PROCESO DE CREACIÓN")

			
def NewOrden(request):
	Usuario=Orden(Usuario=request.user)
	if request.method == 'POST':
		forms=FormOrden(request.POST,instance=Usuario)
		if forms.is_valid():
			forms.save()
			ids=Orden.objects.latest('id')
			return HttpResponse(ids.id)
		else:
			HttpResponse("Ocurrio un Error, contactese con el administrador del sistema.")
	else:
		forms=FormOrden(instance=Usuario)
	return render(request,'movimiento/NewOrden.html',{'forms':forms})
def NewSalida(request):
	Usuario=Salida(Usuario=request.user)
	if request.method == 'POST':
		forms=FormSalida(request.POST,instance=Usuario)
		if forms.is_valid():
			forms.save()
			ids=Salida.objects.latest('id')
			return HttpResponse(ids.id)
		else:
			HttpResponse("Ocurrio un Error, contactese con el administrador del sistema.")
	else:
		forms=FormSalida(instance=Usuario)
	return render(request,'movimiento/NewSalida.html',{'forms':forms})

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

def Salida_detalle(request, id):
	dato = Salida.objects.get(id=int(id))
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
	return render(request, 'movimiento/Salida_detalle.html',dic)

def verConpras(request):
	datos = Orden.objects.all().order_by('-id')
	total = datos.count()
	return render(request,'movimiento/verConpras.html',{'datos':datos,'total':total})
def verSalidas(request):
	datos = Salida.objects.all().order_by('-fecha_salida')
	total = datos.count()
	return render(request,'movimiento/verSalidas.html',{'datos':datos,'total':total})

def filtar_ingresos(request):
	proveedores = Proveedor.objects.all().order_by('-id')
	user=User.objects.filter(is_superuser=True, is_staff=True, is_active=True)
	return render(request,'movimiento/filtar_ingresos.html',{'proveedores':proveedores,'user':user})
def filtar_salidas(request):
	proveedores = Vehiculo.objects.all().order_by('-id')
	user=User.objects.filter(is_superuser=True, is_staff=True, is_active=True)
	return render(request,'movimiento/filtar_salidas.html',{'proveedores':proveedores,'user':user})

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
def EditSalida(request, id):
	dato=Salida.objects.get(id=int(id))
	if request.method=='POST':
		forms=FormSalida(request.POST, instance=dato)
		if forms.is_valid():
			forms.save()
			return HttpResponse("El registro se actualizó correctamente.")
	else:
		forms=FormSalida(instance=dato)
	return render(request,'movimiento/EditSalida.html',{'forms':forms,'dato':dato})

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
def buscarSalida(request):
	if request.method=="POST":
		texto=request.POST["salida"]
		print "texto",texto
		busqueda=(
			Q(id__icontains=texto) |
			Q(id__icontains=texto) |
			Q(id__icontains=texto)
		)
		resultados=Salida.objects.filter(busqueda, estado=True).distinct()
		return render(request,'movimiento/buscarSalida.html',{'resultados':resultados})
	else:
		texto=request.GET["salida"]
		busqueda=(
			Q(id__icontains=texto) |
			Q(id__icontains=texto) |
			Q(id__icontains=texto)
		)
		resultados=Salida.objects.filter(busqueda, estado=True).distinct()
		return render(request,'movimiento/buscarSalida.html',{'datos':resultados})
def EditarProductosDeCompra(request, id):
	compra = request.session['sesion']
	ids_deLACompra = compra[0]
	dato=IngresoProducto.objects.get(id=int(id))
	id_producto = Producto.objects.get(id=int(dato.producto_id))	#float(producto.Precio_compra)
	if request.method=='POST':
		IngresoProducto.objects.filter(id=int(id)).update(cantidad=int(request.POST['cantidad']),Precio_unidad=float(id_producto.Precio_compra),fecha_de_vencimiento=datetime.strptime(request.POST['fecha_de_vencimiento'],"%d/%m/%Y"),total=float(id_producto.Precio_compra) * float(request.POST['cantidad']))
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

		ant_stock = id_producto.Stock
		actual=(id_producto.Stock + int(request.POST['cantidad'])) - id_producto.Stock
		Imvercion_Producto = int(id_producto.Precio_compra) * int(actual)
		Producto.objects.filter(id=int(id_producto.id)).update(Stock=actual,total=Imvercion_Producto)

		
		return HttpResponse("<div class='alert alert-success' role='alert'>El registro de actualizó correctamente</div>")
	else:
		forms=FormIngreso(instance=dato)
	return render(request,'movimiento/EditarProductosDeCompra.html',{'forms':forms,'dato':dato,'compra':ids_deLACompra})
def EditarProductosDeSalida(request, id):
	compra = request.session['sesion']
	ids_deLACompra = compra[0]
	dato=SalidaProducto.objects.get(id=int(id))
	anterior_cantidad = dato.cantidad ##optengo la cantidad anterior de la salida
	id_producto = Producto.objects.get(id=int(dato.producto_id))	#float(producto.Precio_compra)
	if request.method=='POST':
		SalidaProducto.objects.filter(id=int(id)).update(cantidad=int(request.POST['cantidad']),Precio_venta=float(id_producto.Precio_venta),total=float(id_producto.Precio_venta) * float(request.POST['cantidad']))
		salidas = Salida.objects.get(id=int(ids_deLACompra))
		
		t_Paquetes = 0
		Metas = 0
		Avanse = 0
		Porsentaje = 0
		total_pago = 0

		for i in salidas.salidas.all():
			t_Paquetes = i.cantidad + t_Paquetes
			# t_sin_descuento = i.total + t_sin_descuento
			# descuento = t_sin_descuento * 0.18
			total_pago = i.total + total_pago


		Salida.objects.filter(id=int(ids_deLACompra)).update(Total=t_Paquetes,Total_a_pagar=total_pago)
		ant_stock = id_producto.Stock
		#actual=(id_producto.Stock + int(request.POST['cantidad'])) - ant_stock
		actual =  ant_stock - (int(request.POST['cantidad']) - anterior_cantidad )  
		Imvercion_Producto = int(id_producto.Precio_venta) * int(actual)
		Producto.objects.filter(id=int(id_producto.id)).update(Stock=actual,total=Imvercion_Producto)

		
		return HttpResponse("<div class='alert alert-success' role='alert'>El registro de actualizó correctamente</div>")
	else:
		forms=FormSalidaMovil(instance=dato)
	return render(request,'movimiento/EditarProductosDeSalida.html',{'forms':forms,'dato':dato,'compra':ids_deLACompra})


def EliminarProductosDeCompra(request,id):
	dato=IngresoProducto.objects.get(id=int(id))
	compra = request.session['sesion']
	ids_deLACompra = compra[0]
	print "Is de la compra",ids_deLACompra
	return render(request,'movimiento/EliminarProductosDeCompra.html',{'dato':dato,'ids_deLACompra':ids_deLACompra})	

def EliminarProductosDeSalida(request, id):
	dato=SalidaProducto.objects.get(id=int(id))
	compra = request.session['sesion']
	ids_deLACompra = compra[0]
	print "Is de la compra",ids_deLACompra #es el ID de la salida
	return render(request,'movimiento/EliminarProductosDeSalida.html',{'dato':dato,'ids_deLACompra':ids_deLACompra})	

def Eliminar_ingreso(request, id):
	dato=IngresoProducto.objects.get(id=int(id))
	id_producto = Producto.objects.get(id=int(dato.producto_id))#obtengo el producto
	compra = request.session['sesion']
	ids_deLACompra = compra[0]
	print "Id de la compra",ids_deLACompra
	ingresos = Orden.objects.get(id=int(ids_deLACompra))
	ingresos.ingreso.remove(id)
	dato.delete()#elimino completamente el dato

	ant_stock = id_producto.Stock
	actual= int(id_producto.Stock) - int(dato.cantidad)
	Imvercion_Producto = int(id_producto.Precio_compra) * int(actual)
	Producto.objects.filter(id=int(id_producto.id)).update(Stock=actual,total=Imvercion_Producto)
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
def Eliminar_salida(request, id):
	dato=SalidaProducto.objects.get(id=int(id))
	id_producto = Producto.objects.get(id=int(dato.producto_id))#obtengo el producto
	compra = request.session['sesion']
	ids_deLACompra = compra[0]
	print "Id de la compra",ids_deLACompra
	salidas = Salida.objects.get(id=int(ids_deLACompra))
	salidas.salidas.remove(id)
	dato.delete()#elimino completamente el dato

	ant_stock = id_producto.Stock
	actual= int(id_producto.Stock) + int(dato.cantidad)
	Imvercion_Producto = int(id_producto.Precio_compra) * int(actual)
	Producto.objects.filter(id=int(id_producto.id)).update(Stock=actual,total=Imvercion_Producto)
	t_Paquetes = 0
	Metas = 0
	Avanse = 0
	Porsentaje = 0
	total_pago = 0

	for i in salidas.salidas.all():
		t_Paquetes = i.cantidad + t_Paquetes
		# t_sin_descuento = i.total + t_sin_descuento
		# descuento = t_sin_descuento * 0.18
		total_pago = i.total + total_pago
	Salida.objects.filter(id=int(ids_deLACompra)).update(Total=t_Paquetes,Total_a_pagar=total_pago)
	return HttpResponse("Se eliminó la información correctamente")

def EliminarCompra(request, id):
	dato=Orden.objects.get(id=int(id))
	return render(request,'movimiento/EliminarCompra.html',{'dato':dato})	
def Eliminar_Compra(request, id):
	dato=Orden.objects.get(id=int(id))
	dato.delete()
	return HttpResponse("Se eliminó la información correctamente")

def EliminarSalida(request, id):
	dato=Salida.objects.get(id=int(id))
	return render(request,'movimiento/EliminarSalida.html',{'dato':dato})	
def Eliminar_Salida(request, id):
	dato=Salida.objects.get(id=int(id))
	dato.delete()
	return HttpResponse("Se eliminó la información correctamente")

def VerMovimientos(request):
	#filter(fecha_registro__range=(inicio,final))
	ingresos = IngresoProducto.objects.filter(estado=True).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'),Cantidad_ing=Count('producto'))
	salidas = SalidaProducto.objects.filter(estado=True).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'),Cantidad_sali=Count('producto'))
	user=User.objects.filter(is_superuser=True, is_staff=True, is_active=True)
	produc = Producto.objects.filter(estado=True)

	ingresos_total = IngresoProducto.objects.filter(estado=True)
	salidas_total = SalidaProducto.objects.filter(estado=True)
	cant=0
	gastos=0
	t_ingresos=0
	cant_ingresos=0
	for i in ingresos_total:
		cant = cant + i.cantidad
		gastos = gastos + i.total
	ca=0
	gas=0
	t_ing=0
	for i in salidas_total:
		ca = ca + i.cantidad
		gas = gas + i.total	
	# 
	# for i in ingresos:
	# 	print i[int(Cantidad_ing)]
	# 	#print i.Total
	# 	for j in i.items():
			
	# 		for a in j:
	# 			pass
	# 			#print a.Cantidad_ing

	dic={
		'ingresos':ingresos,
		'salidas':salidas,
		'produc':produc,
		't_salidas':salidas.count(),
		't_ingresos':ingresos.count(),
		'cantt':cant,
		'gastoss':gastos,
		'cant':ca,
		'gastos':gas,
		'user':user
	}
	return render(request,'movimiento/VerMovimientos.html',dic)

def ReporteGeneral(request):
	if request.method == 'POST':
		inicio=datetime.strptime(request.POST['inicio'],"%d/%m/%Y")
		final=datetime.strptime(request.POST['final'],"%d/%m/%Y")
		if str(inicio) > str(final):
			return HttpResponse("Error: La Fecha Inicio No pueder ser Mayor a la Fecha Final.")
		final = final + timedelta(days=1)
		
		if int(request.POST['usuario']) == 0:
			ingresos = IngresoProducto.objects.filter(fecha_registro__range=(inicio,final),estado=True).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'),Cantidad_ing=Count('producto'))
			salidas = SalidaProducto.objects.filter(fecha_registro__range=(inicio,final),estado=True).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'),Cantidad_sali=Count('producto'))
			
			produc = Producto.objects.filter(estado=True)

			ingresos_total = IngresoProducto.objects.filter(fecha_registro__range=(inicio,final),estado=True)
			salidas_total = SalidaProducto.objects.filter(fecha_registro__range=(inicio,final),estado=True)
			
			cant=0
			gastos=0
			t_ingresos=0
			cant_ingresos=0
			for i in ingresos_total:
				cant = cant + i.cantidad
				gastos = gastos + i.total

			ca=0
			gas=0
			t_ing=0
			for i in salidas_total:
				ca = ca + i.cantidad
				gas = gas + i.total	

			dic={
				'ingresos':ingresos,
				'salidas':salidas,
				'produc':produc,
				't_salidas':salidas.count(),
				't_ingresos':ingresos.count(),
				'cant':cant,
				'gastos':gastos,
				'cant':ca,
				'gastos':gas
			}
			return render(request,'movimiento/ReporteGeneral.html',dic)
		else:
			user=int(request.POST['usuario'])
			ingresos = IngresoProducto.objects.filter(Usuario_id=user,fecha_registro__range=(inicio,final),estado=True).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'),Cantidad_ing=Count('producto'))
			salidas = SalidaProducto.objects.filter(Usuario_id=user,fecha_registro__range=(inicio,final),estado=True).values('producto').annotate(Total=Sum('cantidad'),pago=Sum('total'),Cantidad_sali=Count('producto'))
			
			produc = Producto.objects.filter(estado=True)

			ingresos_total = IngresoProducto.objects.filter(fecha_registro__range=(inicio,final),estado=True)
			salidas_total = SalidaProducto.objects.filter(fecha_registro__range=(inicio,final),estado=True)
			
			cant=0
			gastos=0
			t_ingresos=0
			cant_ingresos=0
			for i in ingresos_total:
				cant = cant + i.cantidad
				gastos = gastos + i.total

			ca=0
			gas=0
			t_ing=0
			for i in salidas_total:
				ca = ca + i.cantidad
				gas = gas + i.total

			dic={
				'ingresos':ingresos,
				'salidas':salidas,
				'produc':produc,
				't_salidas':salidas.count(),
				't_ingresos':ingresos.count(),
				'cant':cant,
				'gastos':gastos,
				'cant':ca,
				'gastos':gas
			}
		return render(request,'movimiento/ReporteGeneral.html',dic)
def InprimirReporteGeneral(request, user,inicio,fin):
	return HttpResponse("En proceso de creación")