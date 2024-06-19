from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from .models import Alumno
from .forms import AlumnoForm
from docx import Document
import os

def index(request):
    alumno_id = request.GET.get('id')
    if alumno_id:
        alumno = get_object_or_404(Alumno, id=alumno_id)
    else:
        alumno = Alumno.objects.last()

    next_alumno = Alumno.objects.filter(id__gt=alumno.id).order_by('id').first()
    prev_alumno = Alumno.objects.filter(id__lt=alumno.id).order_by('-id').first()

    context = {
        'alumno': alumno,
        'next_alumno': next_alumno,
        'prev_alumno': prev_alumno
    }
    return render(request, 'index.html', context)

def alumno_edit(request, id):
    alumno = get_object_or_404(Alumno, id=id)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            return redirect(reverse('index') + f'?id={alumno.id}')
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
