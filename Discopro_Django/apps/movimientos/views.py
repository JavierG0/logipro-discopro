import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from apps.motoristas.models import Motorista, Sucursal
from apps.usuarios.permissions import administrador_requerido, puede_gestionar_flota
from .models import Movimiento
from .utils import filtrar_movimientos, validar_asignacion_movimiento


@login_required(login_url='usuarios:login')
def lista_movimientos(request):
    """Redirige al dashboard; el listado se gestiona desde allí."""
    return redirect('home')


@login_required(login_url='usuarios:login')
def detalle_movimiento(request, pk):
    """Detalle de un movimiento"""
    movimiento = get_object_or_404(Movimiento, pk=pk)
    return render(request, 'movimiento_detalle.html', {
        'movimiento': movimiento,
        'puede_gestionar_flota': puede_gestionar_flota(request.user),
    })


@login_required(login_url='usuarios:login')
def crear_movimiento(request):
    """Crear nuevo movimiento (redirige al dashboard; validación centralizada en home)."""
    return redirect('home')


@login_required(login_url='usuarios:login')
@administrador_requerido
def editar_movimiento(request, pk):
    """Editar movimiento"""
    movimiento = get_object_or_404(Movimiento.objects.select_related('sucursal'), pk=pk)
    sucursales = Sucursal.objects.filter(activo=True).order_by('nombre')

    if request.method == 'POST':
        movimiento.numero_despacho = request.POST.get('numero_despacho', movimiento.numero_despacho).strip()
        sucursal_id = request.POST.get('sucursal_origen')
        motorista_id = request.POST.get('motorista')
        movimiento.direccion_destino = request.POST.get('direccion_destino', movimiento.direccion_destino).strip()

        sucursal = movimiento.sucursal
        if sucursal_id:
            sucursal = get_object_or_404(Sucursal, pk=sucursal_id, activo=True)
            movimiento.sucursal = sucursal
            movimiento.direccion_origen = sucursal.direccion_completa or sucursal.direccion

        if motorista_id:
            motorista = Motorista.objects.filter(pk=motorista_id, activo=True).select_related('usuario__user').first()
            error = validar_asignacion_movimiento(motorista, sucursal)
            if error:
                messages.error(request, error)
                return render(request, 'movimiento_editar.html', {
                    'movimiento': movimiento,
                    'sucursales': sucursales,
                })
            movimiento.motorista = motorista
        elif sucursal and movimiento.motorista_id:
            error = validar_asignacion_movimiento(movimiento.motorista, sucursal)
            if error:
                messages.error(request, error)
                return render(request, 'movimiento_editar.html', {
                    'movimiento': movimiento,
                    'sucursales': sucursales,
                })

        movimiento.save()
        messages.success(request, 'Movimiento actualizado exitosamente.')
        return redirect('movimientos:detalle', pk=movimiento.pk)

    return render(request, 'movimiento_editar.html', {
        'movimiento': movimiento,
        'sucursales': sucursales,
    })


@login_required(login_url='usuarios:login')
@administrador_requerido
def completar_movimiento(request, pk):
    """El flujo actual no maneja cierre de entregas desde administración."""
    return redirect('movimientos:detalle', pk=pk)


@login_required(login_url='usuarios:login')
def exportar_movimientos(request):
    """Exportar movimientos a un archivo Excel compatible."""
    movimientos = Movimiento.objects.select_related('motorista__usuario__user', 'sucursal').order_by('-creado_en')
    movimientos = filtrar_movimientos(movimientos, request.GET)

    response = HttpResponse(content_type='application/vnd.ms-excel; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="movimientos.xls"'
    response.write('\ufeff')

    writer = csv.writer(response, delimiter='\t')
    writer.writerow([
        'Código Despacho', 'Farmacia Origen', 'Dirección Origen', 'Dirección Destino',
        'Motorista', 'Estado', 'Fecha Registro'
    ])

    for movimiento in movimientos:
        motorista_nombre = movimiento.motorista.usuario.user.get_full_name() if movimiento.motorista else 'Sin asignar'
        farmacia_nombre = movimiento.sucursal.nombre if movimiento.sucursal else 'Sin farmacia'
        writer.writerow([
            movimiento.numero_despacho,
            farmacia_nombre,
            movimiento.direccion_origen,
            movimiento.direccion_destino,
            motorista_nombre,
            movimiento.get_estado_display(),
            movimiento.creado_en.strftime('%d/%m/%Y %H:%M') if movimiento.creado_en else '',
        ])

    return response
