from django import forms
from .models import Alumno, Equivalencias2010, Equivalencias2021, EntrePlanes


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = '__all__'


class Equivalencias2010Form(forms.ModelForm):
    class Meta:
        model = Equivalencias2010
        fields = [
            'nombre', 'equivalencia', 'carrera'
        ]


class Equivalencias2021Form(forms.ModelForm):
    class Meta:
        model = Equivalencias2021
        fields = [
            'nombre', 'equivalencia', 'carrera'
        ]


class EntrePlanesForm(forms.ModelForm):
    class Meta:
        model = EntrePlanes
        fields = [
            'nombre', 'equivalencia', 'carrera'
        ]
