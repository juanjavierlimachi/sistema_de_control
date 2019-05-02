from django.conf.urls import url
from django.contrib import admin
from .views import *
urlpatterns = [
    url(r'^ingresa_productos/(?P<id>\d+)/(?P<ids>\d+)/$', ingresa_productos),
    
    url(r'^salida_productos/(?P<id>\d+)/(?P<ids>\d+)/$', salida_productos),
    url(r'^verIngresos/$', verIngresos),
    
    url(r'^ControlStock/$', ControlStock),
    
    url(r'^stock_de_productos/(?P<id>\d+)/$', stock_de_productos),
    url(r'^ImprimiarStock/(?P<id>\d+)/$', ImprimiarStock),
    url(r'^consuta_por_fecha_ingresos/$', consuta_por_fecha_ingresos),
    
    url(r'^ReportesIngresos/(?P<id_user>\d+)/(?P<id_pro>\d+)/(?P<inicio>[^/]+)/(?P<final>[^/]+)/$',ReportesIngresos),
    
    url(r'^consuta_por_fecha_salidas/$', consuta_por_fecha_salidas),
    
    url(r'^NewOrden/$', NewOrden),
    
    url(r'^NewSalida/$', NewSalida),
    url(r'^verConpras/$', verConpras),
    
    url(r'^verSalidas/$', verSalidas),
    url(r'^NewOrden_detalle/(?P<id>\d+)/$', NewOrden_detalle),
    
    url(r'^Salida_detalle/(?P<id>\d+)/$', Salida_detalle),
    url(r'^filtar_ingresos/$', filtar_ingresos),
    
    url(r'^filtar_salidas/$', filtar_salidas),
    url(r'^EditCompra/(?P<id>\d+)/$',EditCompra),
    
    url(r'^EditSalida/(?P<id>\d+)/$',EditSalida),
    url(r'^consuta_ingresos_por_proveedor/$', consuta_ingresos_por_proveedor),
    
    url(r'^buscarCompra/$', buscarCompra),
    
    url(r'^EditarProductosDeCompra/(?P<id>\d+)/$',EditarProductosDeCompra),
    url(r'^EliminarProductosDeCompra/(?P<id>\d+)/$',EliminarProductosDeCompra),
    
    url(r'^EliminarCompra/(?P<id>\d+)/$',EliminarCompra),
    url(r'^Eliminar_Compra/(?P<id>\d+)/$',Eliminar_Compra),
    
    url(r'^EliminarSalida/(?P<id>\d+)/$',EliminarSalida),
    
    url(r'^Eliminar_Salida/(?P<id>\d+)/$',Eliminar_Salida),
    url(r'^Eliminar_ingreso/(?P<id>\d+)/$',Eliminar_ingreso),
    #url(r'^consuta_por_fecha/(?P<id_proveedor>\d+)/(?P<id_user>\d+)/(?P<inicio>[^/]+)/(?P<fin>[^/]+)/$',consuta_por_fecha),
]