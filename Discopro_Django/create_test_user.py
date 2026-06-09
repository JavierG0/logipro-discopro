import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discopro.settings')
django.setup()

from django.contrib.auth.models import User
from apps.usuarios.models import Usuario

# Crear user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@discopro.com',
        'first_name': 'Test',
        'last_name': 'User',
        'is_staff': False,
        'is_active': True
    }
)

if created:
    user.set_password('test123')
    user.save()
    print(f"✓ User creado: {user.username}")
else:
    print(f"✓ User existe: {user.username}")

# Crear Usuario
usuario, created = Usuario.objects.get_or_create(
    user=user,
    defaults={
        'rut': '12345678-9',
        'telefono': '555-0001',
        'rol': 'motorista',
        'estado': True
    }
)

if created:
    print(f"✓ Usuario creado para {user.username}")
else:
    print(f"✓ Usuario existe para {user.username}")

print("\nCredenciales de prueba:")
print("Usuario: testuser")
print("Contraseña: test123")
