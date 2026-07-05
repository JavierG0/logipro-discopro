from django.db import models


def motorista_pertenece_a_farmacia(motorista, sucursal):
    """El motorista solo puede operar despachos de la farmacia a la que está asignado."""
    if not motorista or not sucursal:
        return False
    return motorista.asignaciones.filter(activa=True, sucursal_id=sucursal.pk).exists()


def validar_asignacion_movimiento(motorista, sucursal):
    """Retorna mensaje de error o None si la asignación es válida."""
    if not motorista:
        return 'Seleccione un motorista válido.'
    if not sucursal:
        return 'Seleccione una farmacia de origen válida.'
    if not motorista_pertenece_a_farmacia(motorista, sucursal):
        nombre_farmacia = sucursal.nombre
        asignacion = motorista.asignaciones.filter(activa=True).select_related('sucursal').first()
        if asignacion and asignacion.sucursal_id:
            return (
                f'El motorista {motorista.usuario.user.get_full_name()} está asignado a '
                f'"{asignacion.sucursal.nombre}" y no puede operar despachos de "{nombre_farmacia}".'
            )
        return f'El motorista no tiene asignación activa en la farmacia "{nombre_farmacia}".'
    return None


def filtrar_movimientos(queryset, params):
    q_despacho = (params.get('q_despacho') or '').strip()
    q_direccion = (params.get('q_direccion') or '').strip()

    if q_despacho:
        queryset = queryset.filter(numero_despacho__icontains=q_despacho)
    if q_direccion:
        queryset = queryset.filter(
            models.Q(direccion_destino__icontains=q_direccion)
            | models.Q(direccion_origen__icontains=q_direccion)
        )
    return queryset
