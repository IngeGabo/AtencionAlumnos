from django.db import models
from django.utils import timezone

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, default='')
    fecha = models.DateTimeField(default=timezone.now)
    boleta = models.IntegerField()
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15)
    plan = models.IntegerField()
    asunto = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=350)

    def __str__(self):
        return self.nombre