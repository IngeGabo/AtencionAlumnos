from django.db.models import Q
from .models import Equivalencias2021
from django.core.exceptions import ValidationError
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from .models import Alumno, Equivalencias2010, Equivalencias2021, EntrePlanes
from .forms import AlumnoForm, Equivalencias2010Form, Equivalencias2021Form, EntrePlanesForm
from docx import Document
import os
from django.utils import timezone
from django.db.models import Q

GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxK1mG1xFjrX-8fyouZfdSoZpVn6CAVk4kTGYFWv-PmBykd-IRRnwtABq8FI8i1njd6/exec'

# -------------------------------
# Vistas para el modelo Alumno
# -------------------------------


def index(request):
    query = request.GET.get('q')
    alumno_id = request.GET.get('id')

    # Bandera para la búsqueda
    buscar_activado = False

    # Lista para almacenar los alumnos
    if query:
        # Activar la bandera de búsqueda
        buscar_activado = True

        # Filtrar los alumnos según la consulta
        alumnos = Alumno.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(boleta__icontains=query) |
            Q(plan__icontains=query) |
            Q(asunto__icontains=query) |
            Q(tipo__icontains=query) |
            Q(descripcion__icontains=query)
        )
    else:
        # Si no hay consulta, obtener todos los alumnos
        alumnos = Alumno.objects.all()

    # Si se ha proporcionado un ID específico, se obtiene ese alumno
    if alumno_id:
        alumno = get_object_or_404(Alumno, id=alumno_id)
    else:
        # Seleccionar el último alumno como predeterminado si no se proporciona un ID
        alumno = alumnos.last() if alumnos else None

    # Navegación entre registros
    next_alumno = Alumno.objects.filter(id__gt=alumno.id).order_by(
        'id').first() if alumno else None
    prev_alumno = Alumno.objects.filter(id__lt=alumno.id).order_by(
        '-id').first() if alumno else None

    # Obtener los últimos registros desde Google Sheets
    try:
        response = requests.get(GOOGLE_SCRIPT_URL)
        response.raise_for_status()
        records = response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching records: {e}")
        records = []

    # Contexto para renderizar en la plantilla
    context = {
        'alumnos': alumnos,  # Pasar la lista completa de alumnos al contexto
        'alumno': alumno,
        'next_alumno': next_alumno,
        'prev_alumno': prev_alumno,
        'records': records,
        'buscar_activado': buscar_activado,  # Pasar la bandera al contexto
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
    doc_path = os.path.join(settings.BASE_DIR, 'AtencionInformatica',
                            'templates', 'atencionalumnos', 'Plantilla.docx')
    doc = Document(doc_path)

    # Reemplazar los valores en la plantilla
    replacements = {
        '{id}': str(alumno.id),
        '{nombre}': alumno.nombre,
        '{apellido}': alumno.apellido,
        '{fecha}': alumno.fecha.strftime('%d/%m/%Y'),
        '{boleta}': str(alumno.boleta),
        '{email}': alumno.email,
        '{telefono}': alumno.telefono,
        '{plan}': str(alumno.plan),
        '{asunto}': alumno.asunto,
        '{tipo}': alumno.tipo,
        '{descripcion}': alumno.descripcion,
    }

    for p in doc.paragraphs:
        for key, value in replacements.items():
            if key in p.text:
                p.text = p.text.replace(key, value)

    # Guardar el documento temporalmente
    tmp_doc_path = os.path.join(
        settings.MEDIA_ROOT, f'alumno_{alumno.id}.docx')
    doc.save(tmp_doc_path)

    # Leer el archivo de Word y enviarlo como respuesta para descarga
    with open(tmp_doc_path, 'rb') as doc_file:
        response = HttpResponse(doc_file.read(
        ), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="alumno_{alumno.id}.docx"'

    # Eliminar el documento temporal
    os.remove(tmp_doc_path)

    return response


def add_record_to_db(request):
    if request.method == 'POST':
        records = request.POST.getlist('record')
        for record in records:
            fields = record.split(',')
            if len(fields) < 10:
                return render(request, 'error.html', {'message': 'Error: El registro no tiene suficientes campos.'})

            try:
                # Asignar los valores a las variables de acuerdo con el orden proporcionado
                # "Marca temporal" está en fields[0] y se ignora
                nombre = fields[1]
                boleta_value = fields[2]
                telefono = fields[3]
                plan_value = fields[4]
                asunto = fields[5]
                tipo = fields[6]
                descripcion = fields[7]
                email = fields[8]
                apellido = fields[9]

                # Verificar que 'boleta' sea un número y esté dentro del rango permitido
                if not boleta_value.isdigit():
                    return render(request, 'error.html', {'message': 'Error: Boleta debe ser un número.'})

                boleta = int(boleta_value)
                if boleta < -9223372036854775808 or boleta > 9223372036854775807:  # Rango para BigInteger
                    return render(request, 'error.html', {'message': 'Error: Boleta fuera de rango permitido.'})

                # Verificar que 'plan' sea un número
                if plan_value.isdigit():
                    plan = int(plan_value)
                else:
                    return render(request, 'error.html', {'message': 'Error: Plan debe ser un número.'})

                # Crear un nuevo objeto Alumno
                Alumno.objects.create(
                    nombre=nombre,
                    apellido=apellido,
                    fecha=timezone.now(),
                    boleta=boleta,
                    email=email,
                    telefono=telefono,
                    plan=plan,
                    asunto=asunto,
                    tipo=tipo,
                    descripcion=descripcion
                )
            except (ValueError, IndexError, ValidationError) as e:
                print(f"Error creating Alumno: {e}")
                return render(request, 'error.html', {'message': f'Error creating Alumno: {e}'})
        return redirect('AtencionInformatica:index')
    else:
        return render(request, 'error.html', {'message': 'Invalid request method'})


def fetch_latest_records(request):
    try:
        response = requests.get(GOOGLE_SCRIPT_URL)
        response.raise_for_status()
        records = response.json()
        return render(request, 'latest_records.html', {'records': records})
    except requests.exceptions.RequestException as e:
        return render(request, 'error.html', {'message': f'Error fetching records from Google Sheets: {e}'})

# -------------------------------------
# Vistas para Equivalencias 2010
# -------------------------------------


def equivalencias_2010_list(request):
    equivalencias = Equivalencias2010.objects.all()
    return render(request, 'equivalencias/equivalencias_2010_list.html', {'equivalencias': equivalencias})


def equivalencia_2010_add(request):
    if request.method == 'POST':
        form = Equivalencias2010Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AtencionInformatica:equivalencias_2010_list')
    else:
        form = Equivalencias2010Form()
    return render(request, 'equivalencias/equivalencias_2010_form.html', {'form': form})


def equivalencias_2010_edit(request, id):
    equivalencia = get_object_or_404(Equivalencias2010, id=id)
    if request.method == 'POST':
        form = Equivalencias2010Form(request.POST, instance=equivalencia)
        if form.is_valid():
            form.save()
            return redirect('AtencionInformatica:equivalencias_2010_list')
    else:
        form = Equivalencias2010Form(instance=equivalencia)
    return render(request, 'equivalencias/equivalencias_2010_form.html', {'form': form})

# -------------------------------------
# Vistas para Equivalencias 2021
# -------------------------------------


def equivalencias_2021_list(request):
    equivalencias = Equivalencias2021.objects.all()
    return render(request, 'equivalencias/equivalencias_2021_list.html', {'equivalencias': equivalencias})


def equivalencias_2021_add(request):
    if request.method == 'POST':
        form = Equivalencias2021Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AtencionInformatica:equivalencias_2021_list')
    else:
        form = Equivalencias2021Form()
    return render(request, 'equivalencias/equivalencias_2021_form.html', {'form': form})


def equivalencias_2021_edit(request, id):
    equivalencia = get_object_or_404(Equivalencias2021, id=id)
    if request.method == 'POST':
        form = Equivalencias2021Form(request.POST, instance=equivalencia)
        if form.is_valid():
            form.save()
            return redirect('AtencionInformatica:equivalencias_2021_list')
    else:
        form = Equivalencias2021Form(instance=equivalencia)
    return render(request, 'equivalencias/equivalencias_2021_form.html', {'form': form})

# -------------------------------------
# Vistas para Equivalencias Entre Planes
# -------------------------------------


def entre_planes_list(request):
    equivalencias = EntrePlanes.objects.all()
    return render(request, 'equivalencias/entre_planes_list.html', {'equivalencias': equivalencias})


def entre_planes_add(request):
    if request.method == 'POST':
        form = EntrePlanesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AtencionInformatica:entre_planes_list')
    else:
        form = EntrePlanesForm()
    return render(request, 'equivalencias/entre_planes_form.html', {'form': form})


def entre_planes_edit(request, id):
    equivalencia = get_object_or_404(EntrePlanes, id=id)
    if request.method == 'POST':
        form = EntrePlanesForm(request.POST, instance=equivalencia)
        if form.is_valid():
            form.save()
            return redirect('AtencionInformatica:entre_planes_list')
    else:
        form = EntrePlanesForm(instance=equivalencia)
    return render(request, 'equivalencias/entre_planes_form.html', {'form': form})
