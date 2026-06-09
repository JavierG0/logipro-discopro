import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse
from apps.usuarios.permissions import administrador_requerido
from .models import Movimiento
from .utils import filtrar_movimientos
from apps.motoristas.models import Motorista, Sucursal


@login_required(login_url='usuarios:login')
def lista_movimientos(request):
    """Redirige al dashboard; el listado se gestiona desde allí."""
    return redirect('home')


@login_required(login_url='usuarios:login')
def detalle_movimiento(request, pk):
    """Detalle de un movimiento"""
    movimiento = get_object_or_404(Movimiento, pk=pk)
    return render(request, 'movimiento_detalle.html', {'movimiento': movimiento})


@login_required(login_url='usuarios:login')
def crear_movimiento(request):
    """Crear nuevo movimiento"""
    motoristas = Motorista.objects.filter(activo=True)
    sucursales = Sucursal.objects.filter(activo=True)

    if request.method == 'POST':
        numero_despacho = request.POST.get('numero_despacho', '').strip()
        motorista_id = request.POST.get('motorista')
        sucursal_id = request.POST.get('sucursal')
        tipo_movimiento = request.POST.get('tipo_movimiento')
        descripcion = request.POST.get('descripcion', '').strip()
        observaciones = request.POST.get('observaciones', '').strip()
        fecha_programada_raw = request.POST.get('fecha_programada')

        if not numero_despacho or not tipo_movimiento or not descripcion or not fecha_programada_raw or not sucursal_id:
            messages.error(request, 'Complete todos los campos obligatorios.')
        elif Movimiento.objects.filter(numero_despacho=numero_despacho).exists():
            messages.error(request, 'Ya existe un movimiento con ese número de despacho.')
        else:
            fecha_programada = parse_datetime(fecha_programada_raw)
            if fecha_programada is None:
                messages.error(request, 'La fecha programada no es válida.')
            else:
                if timezone.is_naive(fecha_programada):
                    fecha_programada = timezone.make_aware(fecha_programada)
                motorista = Motorista.objects.filter(pk=motorista_id).first() if motorista_id else None
                sucursal = get_object_or_404(Sucursal, pk=sucursal_id)
                movimiento = Movimiento.objects.create(
                    numero_despacho=numero_despacho,
                    motorista=motorista,
                    sucursal=sucursal,
                    tipo_movimiento=tipo_movimiento,
                    descripcion=descripcion,
                    observaciones=observaciones,
                    fecha_programada=fecha_programada,
                )
                messages.success(request, 'Movimiento creado exitosamente.')
                return redirect('movimientos:detalle', pk=movimiento.pk)

    return render(request, 'movimiento_crear.html', {
        'motoristas': motoristas,
        'sucursales': sucursales
    })


@login_required(login_url='usuarios:login')
@administrador_requerido
def editar_movimiento(request, pk):
    """Editar movimiento"""
    movimiento = get_object_or_404(Movimiento, pk=pk)
    motoristas = Motorista.objects.filter(activo=True)
    sucursales = Sucursal.objects.filter(activo=True)

    if request.method == 'POST':
        movimiento.numero_despacho = request.POST.get('numero_despacho', movimiento.numero_despacho).strip()
        motorista_id = request.POST.get('motorista')
        sucursal_id = request.POST.get('sucursal')
        movimiento.tipo_movimiento = request.POST.get('tipo_movimiento', movimiento.tipo_movimiento)
        movimiento.descripcion = request.POST.get('descripcion', movimiento.descripcion).strip()
        movimiento.observaciones = request.POST.get('observaciones', movimiento.observaciones).strip()
        fecha_programada_raw = request.POST.get('fecha_programada')

        if motorista_id:
            movimiento.motorista = Motorista.objects.filter(pk=motorista_id).first()
        else:
            movimiento.motorista = None

        if sucursal_id:
            movimiento.sucursal = get_object_or_404(Sucursal, pk=sucursal_id)

        if fecha_programada_raw:
            fecha_programada = parse_datetime(fecha_programada_raw)
            if fecha_programada is None:
                messages.error(request, 'La fecha programada no es válida.')
                return render(request, 'movimiento_editar.html', {
                    'movimiento': movimiento,
                    'motoristas': motoristas,
                    'sucursales': sucursales
                })
            if timezone.is_naive(fecha_programada):
                fecha_programada = timezone.make_aware(fecha_programada)
            movimiento.fecha_programada = fecha_programada

        movimiento.save()
        messages.success(request, 'Movimiento actualizado exitosamente.')
        return redirect('movimientos:detalle', pk=movimiento.pk)

    return render(request, 'movimiento_editar.html', {
        'movimiento': movimiento,
        'motoristas': motoristas,
        'sucursales': sucursales
    })


@login_required(login_url='usuarios:login')
@administrador_requerido
def completar_movimiento(request, pk):
    """Completar un movimiento"""
    movimiento = get_object_or_404(Movimiento, pk=pk)
    
    if request.method == 'POST':
        movimiento.estado = 'completado'
        movimiento.fecha_cierre = timezone.now()
        movimiento.comentarios = request.POST.get('comentarios', '')
        movimiento.save()
        messages.success(request, 'Movimiento completado exitosamente')
        return redirect('movimientos:detalle', pk=pk)
    
    return render(request, 'movimiento_completar.html', {'movimiento': movimiento})


@login_required(login_url='usuarios:login')
def exportar_movimientos(request):
    """Exportar movimientos a un archivo Excel compatible."""
    movimientos = Movimiento.objects.select_related(
        'motorista__usuario__user',
        'motorista__moto',
        'sucursal',
    ).order_by('-fecha_programada')
    movimientos = filtrar_movimientos(movimientos, request.GET)

    response = HttpResponse(content_type='application/vnd.ms-excel; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="movimientos.xls"'
    response.write('\ufeff')

    writer = csv.writer(response, delimiter='\t')
    writer.writerow([
        'N° Despacho', 'Producto / Receta', 'Destinatario', 'RUT Destinatario',
        'Teléfono Destinatario', 'Dirección', 'Comuna', 'Región',
        'Motorista', 'Moto', 'Farmacia', 'Tipo', 'Estado',
        'Fecha Programada', 'Observaciones'
    ])

    for movimiento in movimientos:
        motorista_nombre = (
            f"{movimiento.motorista.usuario.user.first_name} {movimiento.motorista.usuario.user.last_name}"
            if movimiento.motorista else 'Sin asignar'
        )
        moto_placa = (
            movimiento.motorista.moto.placa
            if movimiento.motorista and movimiento.motorista.moto else 'Sin asignar'
        )
        writer.writerow([
            movimiento.numero_despacho,
            movimiento.descripcion,
            movimiento.destinatario_nombre,
            movimiento.destinatario_rut,
            movimiento.destinatario_telefono,
            movimiento.destinatario_direccion,
            movimiento.destinatario_comuna,
            movimiento.destinatario_region,
            motorista_nombre,
            moto_placa,
            movimiento.sucursal.nombre if movimiento.sucursal else 'Sin farmacia',
            movimiento.get_tipo_movimiento_display(),
            movimiento.get_estado_display(),
            movimiento.fecha_programada.strftime('%d/%m/%Y %H:%M') if movimiento.fecha_programada else '',
            movimiento.observaciones or ''
        ])

    return response
