import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discopro.settings')
django.setup()

from django.contrib.auth.models import User
from apps.usuarios.models import Usuario

user, created = User.objects.get_or_create(
    username='operador1',
    defaults={
        'email': 'operador1@discopro.com',
        'first_name': 'Usuario',
        'last_name': 'Operador',
        'is_staff': False,
        'is_active': True,
    },
)

if created:
    user.set_password('operador123')
    user.save()
    print(f"✓ Usuario Django creado: {user.username}")
else:
    print(f"✓ Usuario Django existe: {user.username}")

usuario, created = Usuario.objects.get_or_create(
    user=user,
    defaults={
        'rut': '98765432-1',
        'telefono': '56900000000',
        'rol': 'operador',
        'estado': True,
    },
)

if not created and usuario.rol != 'operador':
    usuario.rol = 'operador'
    usuario.save(update_fields=['rol'])
    print(f"✓ Rol actualizado a operador para {user.username}")
elif created:
    print(f"✓ Perfil operador creado para {user.username}")
else:
    print(f"✓ Perfil operador ya existe para {user.username}")

print("\nCredenciales operador:")
print("Usuario: operador1")
print("Contraseña: operador123")
