from .permissions import es_administrador_sistema, es_operador, puede_gestionar_flota, obtener_rol

ROL_ETIQUETAS = {
    'administrador': 'Administrador del sistema',
    'supervisor': 'Supervisor / Gerencia',
    'operador': 'Operadora',
    'motorista': 'Motorista',
}


def permisos_usuario(request):
    user = request.user
    rol = obtener_rol(user) if user.is_authenticated else None
    motorista_farmacia = None
    if rol == 'motorista' and user.is_authenticated:
        try:
            from apps.motoristas.models import Motorista
            motorista = Motorista.objects.select_related('usuario__user').prefetch_related(
                'asignaciones__sucursal'
            ).get(usuario__user=user)
            sucursal = motorista.sucursal_actual
            if sucursal:
                motorista_farmacia = sucursal.nombre
        except Exception:
            pass
    return {
        'user_rol': rol,
        'user_rol_etiqueta': ROL_ETIQUETAS.get(rol, rol) if rol else None,
        'motorista_farmacia': motorista_farmacia,
        'es_operador': es_operador(user) if user.is_authenticated else False,
        'puede_gestionar_flota': puede_gestionar_flota(user) if user.is_authenticated else False,
        'es_administrador_sistema': es_administrador_sistema(user) if user.is_authenticated else False,
    }
