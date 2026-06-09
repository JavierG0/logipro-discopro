from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from django.db.models import Count, Avg, Q
from datetime import datetime, timedelta
from .models import Reporte
from apps.movimientos.models import Movimiento
from apps.motoristas.models import Motorista


@login_required(login_url='usuarios:login')
def lista_reportes(request):
    """Listado de reportes"""
    reportes = Reporte.objects.all()
    
    tipo = request.GET.get('tipo')
    if tipo:
        reportes = reportes.filter(tipo=tipo)
    
    return render(request, 'reportes.html', {
        'reportes': reportes,
        'tipos': Reporte.TIPOS_REPORTE
    })


@login_required(login_url='usuarios:login')
def detalle_reporte(request, pk):
    """Detalle de un reporte"""
    reporte = get_object_or_404(Reporte, pk=pk)
    return render(request, 'reporte_detalle.html', {'reporte': reporte})


@login_required(login_url='usuarios:login')
def generar_reporte(request):
    """Generar nuevo reporte"""
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        # Generar datos según tipo de reporte
        if tipo == 'movimientos':
            movimientos = Movimiento.objects.filter(
                fecha_programada__range=[fecha_inicio, fecha_fin]
            )
            datos = {
                'total': movimientos.count(),
                'por_estado': dict(movimientos.values('estado').annotate(count=Count('id')).values_list('estado', 'count')),
                'por_tipo': dict(movimientos.values('tipo_movimiento').annotate(count=Count('id')).values_list('tipo_movimiento', 'count')),
            }
            titulo = f"Reporte de Movimientos {fecha_inicio} a {fecha_fin}"
        
        elif tipo == 'motoristas':
            motoristas = Motorista.objects.all()
            datos = {
                'total_motoristas': motoristas.count(),
                'disponibles': motoristas.filter(estado='disponible').count(),
                'en_ruta': motoristas.filter(estado='en_ruta').count(),
                'inactivos': motoristas.filter(estado='inactivo').count(),
                'calificacion_promedio': motoristas.aggregate(Avg('calificacion_promedio'))['calificacion_promedio__avg'],
            }
            titulo = f"Reporte de Motoristas al {fecha_fin}"
        
        elif tipo == 'desempenio':
            movimientos = Movimiento.objects.filter(
                fecha_cierre__range=[fecha_inicio, fecha_fin],
                estado='completado'
            )
            datos = {
                'total_completados': movimientos.count(),
                'calificacion_promedio': movimientos.aggregate(Avg('calificacion'))['calificacion__avg'],
                'distancia_total': movimientos.aggregate(sum=Sum('distancia_km'))['sum'],
            }
            titulo = f"Reporte de Desempeño {fecha_inicio} a {fecha_fin}"
        
        else:
            datos = {}
            titulo = "Reporte General"
        
        reporte = Reporte.objects.create(
            titulo=titulo,
            tipo=tipo,
            descripcion=f"Reporte generado automáticamente",
            usuario_creador=request.user.usuario_profile,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            datos_json=datos
        )
        
        messages.success(request, 'Reporte generado exitosamente')
        return redirect('reportes:detalle', pk=reporte.pk)
    
    return render(request, 'reporte_generar.html')


@login_required(login_url='usuarios:login')
def descargar_reporte(request, pk):
    """Descargar reporte"""
    reporte = get_object_or_404(Reporte, pk=pk)
    
    if reporte.archivo:
        response = FileResponse(reporte.archivo.open('rb'))
        response['Content-Disposition'] = f'attachment; filename="{reporte.archivo.name}"'
        return response
    
    messages.error(request, 'El reporte no tiene archivo para descargar')
    return redirect('reportes:detalle', pk=pk)


from django.db.models import Sum
