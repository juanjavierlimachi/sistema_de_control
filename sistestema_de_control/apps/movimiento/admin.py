# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(IngresoProducto)
admin.site.register(Orden)

admin.site.register(Vehiculo)
admin.site.register(SalidaProducto)
admin.site.register(Salida)