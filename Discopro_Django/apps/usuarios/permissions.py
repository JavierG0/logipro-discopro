from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import Usuario


def obtener_rol(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser:
        return 'administrador'
    try:
        return user.usuario_profile.rol
    except Usuario.DoesNotExist:
        return None


def es_operador(user):
    return obtener_rol(user) == 'operador'


def es_supervisor(user):
    return obtener_rol(user) == 'supervisor'


def es_administrador_sistema(user):
    rol = obtener_rol(user)
    return user.is_superuser or rol == 'administrador'


def puede_gestionar_flota(user):
    """Administrador y supervisor gestionan farmacias, motos, motoristas y asignaciones."""
    rol = obtener_rol(user)
    return user.is_superuser or rol in ('administrador', 'supervisor')


def puede_registrar_movimientos(user):
    rol = obtener_rol(user)
    return user.is_superuser or rol in ('administrador', 'supervisor', 'operador', 'motorista')


def administrador_requerido(view_func):
    """Admin o supervisor — gestión operativa de flota."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not puede_gestionar_flota(request.user):
            messages.error(request, 'No tiene permisos para acceder a esta sección.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def administrador_sistema_requerido(view_func):
    """Solo administrador del sistema — gestión de usuarios y accesos."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not es_administrador_sistema(request.user):
            messages.error(request, 'Solo el administrador del sistema puede gestionar usuarios.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
