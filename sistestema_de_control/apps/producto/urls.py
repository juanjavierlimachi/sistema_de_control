from django.conf.urls import url
from django.contrib import admin
from .views import *
urlpatterns = [
    
    url(r'^verProductos/$', verProducto),
    url(r'^NewProducto/$', NewProducto),
    
    url(r'^verCategorias/$', verCategorias),
    url(r'^NewCategoria/$', NewCategoria),
    url(r'^kardex/(?P<id>\d+)/$', kardexProducto),
    url(r'^NewProveedor/$', NewProveedor),
    
    url(r'^EditarProveedor/(?P<id>\d+)/$', EditarProveedor), 
    url(r'^VerProveedores/$', VerProveedores),
    url(r'^EliminarProveedor/(?P<id>\d+)/$', EliminarProveedor),
    url(r'^Eliminar_Proveedor/(?P<id>\d+)/$', Eliminar_Proveedor),
    url(r'^AltaProveedor/(?P<id>\d+)/$', AltaProveedor),
    
    url(r'^recuperarProveedor/(?P<id>\d+)/$', recuperarProveedor),
    url(r'^buscar_producto/$', buscar_producto),
    url(r'^buscarProducto/(?P<id>\d+)/$', buscarProducto),   
    url(r'^EditProducto/(?P<id>\d+)/$', EditProducto),
    url(r'^EditCategorias/(?P<id>\d+)/$', EditCategorias),
    url(r'^EliminarCategorias/(?P<id>\d+)/$', EliminarCategorias),
    url(r'^Eliminar_Categoria/(?P<id>\d+)/$', Eliminar_Categoria),
    url(r'^dar_baja_producto/(?P<id>\d+)/$', dar_baja_producto),
    url(r'^Eliminar_producto/(?P<id>\d+)/$', Eliminar_producto),
    
    url(r'^dar_alta/(?P<id>\d+)/$', dar_altaProducto),
    url(r'^recuperarProducto/(?P<id>\d+)/$', recuperarProducto),
    url(r'^AltaCategorias/(?P<id>\d+)/$', AltaCategorias),
    
    url(r'^recuperarCategoria/(?P<id>\d+)/$', recuperarCategoria),
    
    
]