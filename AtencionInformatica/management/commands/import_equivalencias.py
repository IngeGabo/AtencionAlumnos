import pandas as pd
from django.core.management.base import BaseCommand
from AtencionInformatica.models import Equivalencia

class Command(BaseCommand):
    help = 'Importa datos de equivalencias desde un archivo Excel'

    def handle(self, *args, **kwargs):
        file_path = 'E:/Escuela/Servicio Social/Atencion_Alumnos_Alfa2/AtencionAlumnos/AtencionInformatica/templates/atencionalumnos/Equivalencias.xlsx'
        excel_data = pd.ExcelFile(file_path)

        equivalencias_2010 = pd.read_excel(excel_data, sheet_name='Entre_Carrera_2010')
        equivalencias_2021 = pd.read_excel(excel_data, sheet_name='Entre_Carrera_2021')
        equivalencias_inter_planes = pd.read_excel(excel_data, sheet_name='Entre_Planes')

        # Imprimir nombres de columnas para verificación
        print("Columnas en equivalencias_2010:", equivalencias_2010.columns)
        print("Columnas en equivalencias_2021:", equivalencias_2021.columns)
        print("Columnas en equivalencias_inter_planes:", equivalencias_inter_planes.columns)

        # Proceso para equivalencias_2010
        for _, row in equivalencias_2010.iterrows():
            Equivalencia.objects.create(
                plan_origen='2010',
                carrera_origen=row['Unnamed: 1'],
                codigo_origen=row['Unnamed: 2'],
                nombre_origen=row['Unnamed: 3'],
                plan_destino='Otra carrera',
                carrera_destino=row['Unnamed: 4'],
                codigo_destino=row['Unnamed: 5'],
                nombre_destino=row['Unnamed: 6']
            )

        # Proceso para equivalencias_2021
        for _, row in equivalencias_2021.iterrows():
            Equivalencia.objects.create(
                plan_origen='2021',
                carrera_origen=row['Unnamed: 1'],
                codigo_origen=row['Unnamed: 2'],
                nombre_origen=row['Unnamed: 3'],
                plan_destino='Otra carrera',
                carrera_destino=row['Unnamed: 4'],
                codigo_destino=row['Unnamed: 5'],
                nombre_destino=row['Unnamed: 6']
            )

        # Proceso para equivalencias_inter_planes
        for _, row in equivalencias_inter_planes.iterrows():
            Equivalencia.objects.create(
                plan_origen='InterPlan',
                carrera_origen=row['Unnamed: 1'],
                codigo_origen=row['Unnamed: 2'],
                nombre_origen=row['Unnamed: 3'],
                plan_destino='InterPlan',
                carrera_destino=row['Unnamed: 4'],
                codigo_destino='',  # Esta columna no existe en esta hoja
                nombre_destino=row['Unnamed: 4']  # Ajusta esto según tus necesidades
            )

        self.stdout.write(self.style.SUCCESS('Datos importados exitosamente'))

