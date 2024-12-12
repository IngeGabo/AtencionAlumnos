from django.contrib import admin
from .models import Alumno, Equivalencias2010, Equivalencias2021, EntrePlanes


class AlumnoAdmin(admin.ModelAdmin):
    exclude = ('fecha', 'id')
    list_display = ('id', 'nombre', 'apellido', 'fecha', 'boleta',
                    'email', 'telefono', 'plan', 'asunto', 'tipo', 'descripcion')
    search_fields = ['nombre', 'apellido', 'boleta', 'email',
                     'telefono', 'plan', 'asunto', 'tipo', 'descripcion']


class Equivalencias2010Admin(admin.ModelAdmin):
    list_display = ('nombre', 'equivalencia', 'carrera')
    search_fields = ['nombre', 'equivalencia', 'carrera']


class Equivalencias2021Admin(admin.ModelAdmin):
    list_display = ('nombre', 'equivalencia', 'carrera')
    search_fields = ['nombre', 'equivalencia', 'carrera']


class EntrePlanesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'equivalencia', 'carrera')
    search_fields = ['nombre', 'equivalencia', 'carrera']


# Registra los modelos en el panel de administración
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Equivalencias2010, Equivalencias2010Admin)
admin.site.register(Equivalencias2021, Equivalencias2021Admin)
admin.site.register(EntrePlanes, EntrePlanesAdmin)
