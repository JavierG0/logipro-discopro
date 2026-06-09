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


def puede_gestionar_flota(user):
    """Admin y despachador pueden gestionar farmacias, motos y motoristas."""
    rol = obtener_rol(user)
    return user.is_superuser or rol in ('administrador', 'despachador')


def administrador_requerido(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not puede_gestionar_flota(request.user):
            messages.error(request, 'No tiene permisos para acceder a esta sección.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
