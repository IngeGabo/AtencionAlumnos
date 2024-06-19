from django.urls import path
from .views import index, alumno_edit, generate_docx

urlpatterns = [
    path('', index, name='index'),
    path('edit/<int:id>/', alumno_edit, name='alumno_edit'),
    path('docx/<int:id>/', generate_docx, name='generate_docx'),
]