from django.db import models
from django.utils import timezone

from django.db import models


class Equivalencias2010(models.Model):
    nombre = models.CharField(max_length=200)
    equivalencia = models.CharField(max_length=200)
    carrera = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre} - {self.equivalencia} - {self.carrera}"


class Equivalencias2021(models.Model):
    nombre = models.CharField(max_length=200)
    equivalencia = models.CharField(max_length=200)
    carrera = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre} - {self.equivalencia} - {self.carrera}"


class EntrePlanes(models.Model):
    nombre = models.CharField(max_length=200)
    equivalencia = models.CharField(max_length=200)
    carrera = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre} - {self.equivalencia} - {self.carrera}"


class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, default='')
    fecha = models.DateTimeField(default=timezone.now)
    boleta = models.BigIntegerField()
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=50)
    plan = models.IntegerField()
    asunto = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=350)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
