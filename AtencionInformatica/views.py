import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from .models import Alumno
from .forms import AlumnoForm
from docx import Document
import os
import json
from django.utils import timezone

def index(request):
    alumno_id = request.GET.get('id')
    if alumno_id:
        alumno = get_object_or_404(Alumno, id=alumno_id)
    else:
        alumno = Alumno.objects.last()

    next_alumno = Alumno.objects.filter(id__gt=alumno.id).order_by('id').first()
    prev_alumno = Alumno.objects.filter(id__lt=alumno.id).order_by('-id').first()

    # Obtener los últimos registros
    try:
        response = requests.get(GOOGLE_SCRIPT_URL)
        response.raise_for_status()
        records = response.json()

        # Verifica que la estructura del JSON sea la esperada
        if not isinstance(records, list) or len(records) == 0:
            raise ValueError("JSON no contiene una lista o está vacío")
        if not isinstance(records[0], list):
            raise ValueError("El primer elemento del JSON no es una lista")
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching records: {e}")
        records = []

    context = {
        'alumno': alumno,
        'next_alumno': next_alumno,
        'prev_alumno': prev_alumno,
        'records': records,  # Asegúrate de incluir 'records' en el contexto
    }
    return render(request, 'index.html', context)

def alumno_edit(request, id):
    alumno = get_object_or_404(Alumno, id=id)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            return redirect(reverse('AtencionInformatica:index') + f'?id={alumno.id}')
    else:
        form = AlumnoForm(instance=alumno)
    return render(request, 'alumno_edit.html', {'form': form})

def generate_docx(request, id):
    alumno = get_object_or_404(Alumno, id=id)
    
    # Cargar la plantilla de Word
    doc_path = os.path.join(settings.BASE_DIR, 'AtencionInformatica', 'templates', 'atencionalumnos', 'Plantilla.docx')
    doc = Document(doc_path)
    
    # Reemplazar los valores en la plantilla
    for p in doc.paragraphs:
        if '{id}' in p.text:
            p.text = p.text.replace('{id}', str(alumno.id))
        if '{nombre}' in p.text:
            p.text = p.text.replace('{nombre}', alumno.nombre)
        if '{apellido}' in p.text:
            p.text = p.text.replace('{apellido}', alumno.apellido)
        if '{fecha}' in p.text:
            p.text = p.text.replace('{fecha}', alumno.fecha.strftime('%d/%m/%Y'))
        if '{boleta}' in p.text:
            p.text = p.text.replace('{boleta}', str(alumno.boleta))
        if '{email}' in p.text:
            p.text = p.text.replace('{email}', alumno.email)
        if '{telefono}' in p.text:
            p.text = p.text.replace('{telefono}', alumno.telefono)
        if '{plan}' in p.text:
            p.text = p.text.replace('{plan}', str(alumno.plan))
        if '{asunto}' in p.text:
            p.text = p.text.replace('{asunto}', alumno.asunto)
        if '{tipo}' in p.text:
            p.text = p.text.replace('{tipo}', alumno.tipo)
        if '{descripcion}' in p.text:
            p.text = p.text.replace('{descripcion}', alumno.descripcion)
    
    # Guardar el documento temporalmente
    tmp_doc_path = os.path.join(settings.BASE_DIR, 'temp', f'alumno_{alumno.id}.docx')
    doc.save(tmp_doc_path)

    # Leer el archivo de Word y enviarlo como respuesta
    with open(tmp_doc_path, 'rb') as doc_file:
        response = HttpResponse(doc_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="alumno_{alumno.id}.docx"'
    
    # Eliminar el documento temporal
    try:
        os.remove(tmp_doc_path)
    except PermissionError:
        pass

    return response

GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxK1mG1xFjrX-8fyouZfdSoZpVn6CAVk4kTGYFWv-PmBykd-IRRnwtABq8FI8i1njd6/exec'  # Reemplaza con la URL de tu script

def add_record_to_db(request):
    if request.method == 'POST':
        records = request.POST.getlist('record')
        for record in records:
            fields = record.split(',')
            try:
                Alumno.objects.create(
                    nombre=fields[1],
                    apellido=fields[9],
                    fecha=timezone.now(),
                    boleta=int(fields[2]),  # Verifica que boleta sea un número entero
                    email=fields[8],
                    telefono=fields[3],
                    plan=int(fields[4]),  # Verifica que plan sea un número entero
                    asunto=fields[5],
                    tipo=fields[6],
                    descripcion=fields[7]
                )
            except (ValueError, IndexError) as e:
                print(f"Error creating Alumno: {e}")
                return render(request, 'AtencionInformatica/error.html', {'message': f'Error creating Alumno: {e}'})
        return redirect('AtencionInformatica:index')

    return render(request, 'AtencionInformatica/error.html', {'message': 'Invalid request method.'})

def fetch_latest_records(request):
    try:
        response = requests.get(GOOGLE_SCRIPT_URL)
        response.raise_for_status()  # Levanta un error para códigos de estado HTTP 4xx/5xx
        
        try:
            records = response.json()  # Decodifica el JSON
            # Verifica que la estructura del JSON sea la esperada
            if not isinstance(records, list) or len(records) == 0:
                raise ValueError("JSON does not contain a list or is empty")
            if not isinstance(records[0], list):
                raise ValueError("The first element of JSON is not a list")
        except ValueError as e:  # Maneja errores de decodificación JSON
            return render(request, 'AtencionInformatica/error.html', {'message': f'Error decoding JSON: {e}'})
        
        return render(request, 'AtencionInformatica/latest_records.html', {'records': records})
    except requests.exceptions.RequestException as e:
        return render(request, 'AtencionInformatica/error.html', {'message': f'Error fetching records from Google Sheets: {e}'})
