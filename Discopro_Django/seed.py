"""
Script para cargar datos iniciales en la base de datos.
Uso: python manage.py shell < seed.py
"""

from django.contrib.auth.models import User
from apps.usuarios.models import Usuario, Departamento
from apps.motoristas.models import Motorista
from apps.motoristas.models import Sucursal
from apps.movimientos.models import Movimiento
from django.utils import timezone

# Crear departamentos
print("Creando departamentos...")
admin_dept, _ = Departamento.objects.get_or_create(
    codigo='admin',
    defaults={'nombre': 'Administrador'}
)
operador_dept, _ = Departamento.objects.get_or_create(
    codigo='operador',
    defaults={'nombre': 'Operador'}
)
motorista_dept, _ = Departamento.objects.get_or_create(
    codigo='motorista',
    defaults={'nombre': 'Motorista'}
)
supervisor_dept, _ = Departamento.objects.get_or_create(
    codigo='supervisor',
    defaults={'nombre': 'Supervisor'}
)

# Crear usuarios de prueba
print("Creando usuarios...")
usuarios_data = [
    ('admin', 'admin@discopro.com', 'Admin', 'User', admin_dept, True),
    ('operador1', 'operador@discopro.com', 'Operador', 'Test', operador_dept, True),
    ('motorista1', 'motorista1@discopro.com', 'Juan', 'Pérez', motorista_dept, True),
    ('motorista2', 'motorista2@discopro.com', 'Carlos', 'García', motorista_dept, True),
    ('supervisor1', 'supervisor@discopro.com', 'Supervisor', 'Test', supervisor_dept, True),
]

usuarios_dict = {}
for username, email, first_name, last_name, dept, is_active in usuarios_data:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'is_active': is_active,
            'is_staff': dept == admin_dept,
            'is_superuser': dept == admin_dept,
        }
    )
    if created:
        user.set_password('password123')
        user.save()
    
    Usuario.objects.get_or_create(
        user=user,
        defaults={'departamento': dept}
    )
    usuarios_dict[username] = user
    print(f"  ✓ Usuario '{username}' creado")

# Crear sucursales
print("\nCreando sucursales...")
sucursales_data = [
    {
        'nombre': 'Sucursal Centro',
        'direccion': 'Calle Principal 123',
        'ciudad': 'Bogotá',
        'telefono': '3101234567',
        'email': 'centro@discopro.com'
    },
    {
        'nombre': 'Sucursal Norte',
        'direccion': 'Carrera 7 456',
        'ciudad': 'Bogotá',
        'telefono': '3107654321',
        'email': 'norte@discopro.com'
    },
    {
        'nombre': 'Sucursal Sur',
        'direccion': 'Avenida Sur 789',
        'ciudad': 'Bogotá',
        'telefono': '3109876543',
        'email': 'sur@discopro.com'
    },
]

sucursales_dict = {}
for data in sucursales_data:
    sucursal, created = Sucursal.objects.get_or_create(
        nombre=data['nombre'],
        defaults=data
    )
    sucursales_dict[data['nombre']] = sucursal
    if created:
        print(f"  ✓ Sucursal '{data['nombre']}' creada")

# Crear motoristas
print("\nCreando motoristas...")
motoristas_data = [
    {
        'usuario': usuarios_dict['motorista1'],
        'licencia': 'LIC001',
        'vehiculo': 'NQB-123',
        'estado': 'disponible',
        'telefono': '3115555555',
        'ubicacion_actual': '4.7110,-74.0075'
    },
    {
        'usuario': usuarios_dict['motorista2'],
        'licencia': 'LIC002',
        'vehiculo': 'NQB-456',
        'estado': 'disponible',
        'telefono': '3116666666',
        'ubicacion_actual': '4.6726,-74.0481'
    },
]

motoristas_dict = {}
for data in motoristas_data:
    motorista, created = Motorista.objects.get_or_create(
        licencia=data['licencia'],
        defaults=data
    )
    motoristas_dict[data['licencia']] = motorista
    if created:
        print(f"  ✓ Motorista '{data['licencia']}' ({data['usuario'].first_name}) creado")

# Crear movimientos de ejemplo
print("\nCreando movimientos...")
movimientos_data = [
    {
        'despacho_numero': 'DSP001',
        'motorista': motoristas_dict['LIC001'],
        'sucursal': sucursales_dict['Sucursal Centro'],
        'tipo': 'entrega',
        'estado': 'completado',
        'observaciones': 'Entrega realizada a las 10:30',
    },
    {
        'despacho_numero': 'DSP002',
        'motorista': motoristas_dict['LIC002'],
        'sucursal': sucursales_dict['Sucursal Norte'],
        'tipo': 'retiro',
        'estado': 'en_progreso',
        'observaciones': 'En camino al destino',
    },
    {
        'despacho_numero': 'DSP003',
        'motorista': motoristas_dict['LIC001'],
        'sucursal': sucursales_dict['Sucursal Sur'],
        'tipo': 'entrega',
        'estado': 'pendiente',
        'observaciones': 'Pendiente de asignación',
    },
]

for data in movimientos_data:
    movimiento, created = Movimiento.objects.get_or_create(
        despacho_numero=data['despacho_numero'],
        defaults=data
    )
    if created:
        print(f"  ✓ Movimiento '{data['despacho_numero']}' creado")

print("\n✅ Datos iniciales cargados exitosamente!")
print("\nCredenciales de prueba:")
print("  Usuario: motorista1 / Contraseña: password123")
print("  Usuario: operador1 / Contraseña: password123")
print("  Usuario: admin / Contraseña: password123")
