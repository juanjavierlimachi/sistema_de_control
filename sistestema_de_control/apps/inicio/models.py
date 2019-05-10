# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.forms import User
# Create your models here.


class Perfiles(models.Model):
	usuario = models.OneToOneField(User, unique=True, related_name='perfil')
	ci = models.IntegerField()
	telefono = models.IntegerField()
	def __unicode__(self):
		return self.usuario.username

# class Empleado(models.Model):
# 	Usuario = models.OneToOneField(User, unique=True, related_name='Empleado')
# 	ci = models.IntegerField()
# 	telefono = models.IntegerField()
# 	def __unicode__(self):
# 		return self.usuario.username