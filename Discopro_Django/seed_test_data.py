import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discopro.settings')
django.setup()

from apps.motoristas.models import Sucursal, Moto
from apps.usuarios.models import Usuario

# Crear una sucursal por defecto si no existe
sucursal, created = Sucursal.objects.get_or_create(
    nombre='Sucursal Principal',
    defaults={
        'ciudad': 'Lima',
        'direccion': 'Av. Principales 123',
        'telefono': '555-0001',
        'activo': True
    }
)

if created:
    print(f"✓ Sucursal creada: {sucursal.nombre}")
else:
    print(f"✓ Sucursal existe: {sucursal.nombre}")

# Crear una moto de prueba si no existe
moto, created = Moto.objects.get_or_create(
    placa='MOTO-001',
    defaults={
        'marca': 'Honda',
        'modelo': 'Wave',
        'año': 2023,
        'color': 'Rojo',
        'sucursal': sucursal,
        'estado': 'disponible',
        'activo': True
    }
)

if created:
    print(f"✓ Moto creada: {moto}")
else:
    print(f"✓ Moto existe: {moto}")

print("\n✓ Datos de prueba listos!")
