from django.conf.urls import url
from django.contrib import admin
from .views import *
urlpatterns = [
    url(r'^$', inicio),
    url(r'^logueado/$', logueado),
    url(r'^salir/$', salir),
    url(r'^DatosUsuario/$', DatosUsuario, name='listaUsuarios'),
    url(r'^nuevo/$',nuevoUser.as_view(), name='nuevoUser'),
    url(r'^VerUsuario/(?P<id>\d+)/$',VerUsuario),
    url(r'^editarperfil/$',editar_perfil),
    url(r'^editarcontracenia/$',editarcontracenia),
    url(r'^verificacion/$',verificacion, name='verificacion'),
    url(r'^DasactivarUser/$',DasactivarUser),
    url(r'^VolverHavilitar/$',VolverHavilitar),
    url(r'^reset_password/$', reset_password),
    
]