from django.urls import path
from . import views
from .views import equivalencias_2010_edit, equivalencias_2021_add, equivalencias_2021_edit

app_name = 'AtencionInformatica'

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/<int:id>/', views.alumno_edit, name='alumno_edit'),
    path('docx/<int:id>/', views.generate_docx, name='generate_docx'),
    path('latest-records/', views.fetch_latest_records,
         name='fetch_latest_records'),
    path('add-record/', views.add_record_to_db, name='add_record_to_db'),

    # Rutas para equivalencias 2010
    path('equivalencias/2010/add/', views.equivalencia_2010_add,
         name='equivalencia_2010_add'),
    path('equivalencias/2010/', views.equivalencias_2010_list,
         name='equivalencias_2010_list'),
    path('equivalencias/2010/edit/<int:id>/',
         equivalencias_2010_edit, name='equivalencia_2010_edit'),

    # Rutas para equivalencias 2021
    path('equivalencias/2021/add/', equivalencias_2021_add,
         name='equivalencias_2021_add'),
    path('equivalencias/2021/', views.equivalencias_2021_list,
         name='equivalencias_2021_list'),
    path('equivalencias/2021/edit/<int:id>/',
         equivalencias_2021_edit, name='equivalencia_2021_edit'),

    # Rutas para equivalencias entre planes
    path('equivalencias/entre-planes/add/', views.entre_planes_add,
         name='equivalencia_entre_planes_add'),
    path('equivalencias/entre-planes/',
         views.entre_planes_list, name='entre_planes_list'),
    path('equivalencias/entre-planes/edit/<int:id>/',
         views.entre_planes_edit, name='equivalencia_entre_planes_edit'),
]
