from .permissions import es_operador, puede_gestionar_flota, obtener_rol


def permisos_usuario(request):
    user = request.user
    return {
        'user_rol': obtener_rol(user) if user.is_authenticated else None,
        'es_operador': es_operador(user) if user.is_authenticated else False,
        'puede_gestionar_flota': puede_gestionar_flota(user) if user.is_authenticated else False,
    }
