from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.movimientos.models import Movimiento
from apps.usuarios.permissions import obtener_rol
from .models import Motorista


def motorista_requerido(view_func):
    def wrapper(request, *args, **kwargs):
        if obtener_rol(request.user) != 'motorista':
            messages.error(request, 'Este portal es exclusivo para motoristas.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def _motorista_actual(request):
    from django.db.models import Prefetch
    from .models import AsignacionOperativa
    return get_object_or_404(
        Motorista.objects.select_related('usuario__user').prefetch_related(
            Prefetch(
                'asignaciones',
                queryset=AsignacionOperativa.objects.filter(activa=True).select_related('moto', 'sucursal'),
            )
        ),
        usuario__user=request.user,
    )


@login_required(login_url='usuarios:login')
@motorista_requerido
def inicio(request):
    motorista = _motorista_actual(request)
    hoy = timezone.localdate()
    despachos = Movimiento.objects.filter(motorista=motorista)
    stats = {
        'pendientes': despachos.filter(estado='pendiente').count(),
        'en_ruta': despachos.filter(estado='en_ruta').count(),
        'entregados_hoy': despachos.filter(estado='entregado', entregado_en__date=hoy).count(),
        'incidencias': despachos.filter(estado='incidencia').count(),
    }
    primer_pendiente = despachos.filter(estado='pendiente').order_by('creado_en').first()
    primer_en_ruta = despachos.filter(estado='en_ruta').order_by('-actualizado_en').first()
    return render(request, 'motorista_portal/inicio.html', {
        'motorista': motorista,
        'stats': stats,
        'primer_pendiente': primer_pendiente,
        'primer_en_ruta': primer_en_ruta,
    })


@login_required(login_url='usuarios:login')
@motorista_requerido
def mis_despachos(request):
    motorista = _motorista_actual(request)
    despachos = Movimiento.objects.filter(motorista=motorista).exclude(estado='entregado').order_by('-creado_en')
    return render(request, 'motorista_portal/mis_despachos.html', {'motorista': motorista, 'despachos': despachos})


@login_required(login_url='usuarios:login')
@motorista_requerido
def detalle_despacho(request, pk):
    motorista = _motorista_actual(request)
    despacho = get_object_or_404(Movimiento.objects.select_related('sucursal'), pk=pk, motorista=motorista)
    return render(request, 'motorista_portal/detalle_despacho.html', {'motorista': motorista, 'despacho': despacho})


@login_required(login_url='usuarios:login')
@motorista_requerido
def iniciar_ruta(request, pk):
    motorista = _motorista_actual(request)
    despacho = get_object_or_404(Movimiento, pk=pk, motorista=motorista)
    if despacho.estado == 'pendiente':
        despacho.estado = 'en_ruta'
        despacho.save(update_fields=['estado', 'actualizado_en'])
        messages.success(request, 'Ruta iniciada.')
    return redirect('portal_motorista:detalle', pk=despacho.pk)


@login_required(login_url='usuarios:login')
@motorista_requerido
def marcar_entregado(request, pk):
    motorista = _motorista_actual(request)
    despacho = get_object_or_404(Movimiento, pk=pk, motorista=motorista)
    if despacho.estado in ('pendiente', 'en_ruta'):
        despacho.estado = 'entregado'
        despacho.entregado_en = timezone.now()
        despacho.save(update_fields=['estado', 'entregado_en', 'actualizado_en'])
        messages.success(request, 'Despacho marcado como entregado.')
    return redirect('portal_motorista:detalle', pk=despacho.pk)


@login_required(login_url='usuarios:login')
@motorista_requerido
def reportar_incidencia(request, pk):
    motorista = _motorista_actual(request)
    despacho = get_object_or_404(Movimiento, pk=pk, motorista=motorista)
    if request.method == 'POST':
        despacho.estado = 'incidencia'
        despacho.tipo_incidencia = request.POST.get('tipo_incidencia', '')
        despacho.comentario_incidencia = request.POST.get('comentario_incidencia', '').strip()
        despacho.save(update_fields=['estado', 'tipo_incidencia', 'comentario_incidencia', 'actualizado_en'])
        messages.success(request, 'Incidencia registrada.')
        return redirect('portal_motorista:detalle', pk=despacho.pk)
    return render(request, 'motorista_portal/incidencia.html', {
        'motorista': motorista,
        'despacho': despacho,
        'tipos_incidencia': Movimiento.TIPOS_INCIDENCIA,
    })


@login_required(login_url='usuarios:login')
@motorista_requerido
def perfil(request):
    motorista = _motorista_actual(request)
    return render(request, 'motorista_portal/perfil.html', {'motorista': motorista})


@login_required(login_url='usuarios:login')
@motorista_requerido
def mi_moto(request):
    motorista = _motorista_actual(request)
    return render(request, 'motorista_portal/mi_moto.html', {'motorista': motorista})


@login_required(login_url='usuarios:login')
@motorista_requerido
def historial(request):
    motorista = _motorista_actual(request)
    fecha = request.GET.get('fecha')
    despachos = Movimiento.objects.filter(motorista=motorista, estado='entregado').order_by('-entregado_en')
    if fecha:
        despachos = despachos.filter(entregado_en__date=fecha)
    return render(request, 'motorista_portal/historial.html', {
        'motorista': motorista,
        'despachos': despachos,
        'fecha': fecha or '',
    })
