from django.db.models import Q


def filtrar_movimientos(queryset, params):
    q_despacho = (params.get('q_despacho') or '').strip()
    q_motorista = (params.get('q_motorista') or '').strip()
    q_moto = (params.get('q_moto') or '').strip()
    q_fecha = (params.get('q_fecha') or '').strip()
    q_destinatario = (params.get('q_destinatario') or '').strip()

    if q_despacho:
        queryset = queryset.filter(numero_despacho__icontains=q_despacho)
    if q_motorista:
        queryset = queryset.filter(
            Q(motorista__usuario__user__first_name__icontains=q_motorista) |
            Q(motorista__usuario__user__last_name__icontains=q_motorista)
        )
    if q_moto:
        queryset = queryset.filter(motorista__moto__placa__icontains=q_moto)
    if q_fecha:
        queryset = queryset.filter(fecha_programada__date=q_fecha)
    if q_destinatario:
        queryset = queryset.filter(
            Q(destinatario_nombre__icontains=q_destinatario) |
            Q(destinatario_rut__icontains=q_destinatario)
        )
    return queryset
