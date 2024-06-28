from django.urls import path
from . import views

app_name = 'AtencionInformatica'  # Definir app_name aquí

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/<int:id>/', views.alumno_edit, name='alumno_edit'),
    path('docx/<int:id>/', views.generate_docx, name='generate_docx'),
    path('latest-records/', views.fetch_latest_records, name='fetch_latest_records'),
    path('add-record/', views.add_record_to_db, name='add_record_to_db'),
]
