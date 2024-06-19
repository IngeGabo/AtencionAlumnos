from django.contrib import admin
from .models import Alumno

class AlumnoAdmin(admin.ModelAdmin):
    exclude = ('fecha', 'id')
    list_display = ('id','nombre', 'apellido', 'fecha', 'boleta', 'email', 'telefono', 'plan', 'asunto', 'tipo', 'descripcion')
    search_fields = ['nombre', 'apellido', 'boleta', 'email', 'telefono', 'plan', 'asunto', 'tipo', 'descripcion']

admin.site.register(Alumno, AlumnoAdmin)