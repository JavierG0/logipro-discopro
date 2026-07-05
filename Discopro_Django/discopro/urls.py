"""
URL configuration for discopro project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.movimientos.models import Movimiento
from apps.movimientos.utils import filtrar_movimientos, validar_asignacion_movimiento
from apps.motoristas.models import Motorista, Sucursal


def _crear_movimiento_desde_post(request):
    numero_despacho = request.POST.get('numero_despacho', '').strip()
    sucursal_id = request.POST.get('sucursal_origen')
    motorista_id = request.POST.get('motorista')
    direccion_destino = request.POST.get('direccion_destino', '').strip()

    if not numero_despacho or not sucursal_id or not motorista_id or not direccion_destino:
        messages.error(request, 'Complete todos los campos obligatorios.')
        return False

    if Movimiento.objects.filter(numero_despacho=numero_despacho).exists():
        messages.error(request, 'El número de despacho ya existe.')
        return False

    sucursal = get_object_or_404(Sucursal, pk=sucursal_id, activo=True)
    motorista = Motorista.objects.filter(pk=motorista_id, activo=True).select_related('usuario__user').first()
    error = validar_asignacion_movimiento(motorista, sucursal)
    if error:
        messages.error(request, error)
        return False

    Movimiento.objects.create(
        numero_despacho=numero_despacho,
        sucursal=sucursal,
        direccion_origen=sucursal.direccion_completa or sucursal.direccion,
        direccion_destino=direccion_destino,
        motorista=motorista,
    )
    messages.success(
        request,
        f'Despacho {numero_despacho} registrado. Origen: {sucursal.nombre}.',
    )
    return True


@login_required(login_url='usuarios:login')
def home(request):
    sucursales = Sucursal.objects.filter(activo=True).order_by('nombre')
    movimientos = Movimiento.objects.select_related(
        'motorista__usuario__user', 'sucursal'
    ).order_by('-creado_en')
    movimientos = filtrar_movimientos(movimientos, request.GET)

    if not any(request.GET.get(k) for k in ('q_despacho', 'q_direccion')):
        movimientos = movimientos[:20]

    stats = {
        'movimientos': Movimiento.objects.count(),
        'disponibles': Motorista.objects.filter(estado='disponible', activo=True).count(),
    }

    if request.method == 'POST':
        if _crear_movimiento_desde_post(request):
            return redirect('home')

    return render(request, 'dashboard.html', {
        'movimientos': movimientos,
        'sucursales': sucursales,
        'stats': stats,
        'filtros': request.GET,
    })


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='usuarios:login', permanent=False), name='index'),
    path('dashboard/', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('farmacia/', include('apps.motoristas.farmacia_urls')),
    path('portal-motorista/', include('apps.motoristas.portal_urls')),
    path('motoristas/sucursales/', RedirectView.as_view(pattern_name='farmacia:lista', permanent=True)),
    path('motoristas/', include('apps.motoristas.urls')),
    path('movimientos/', include('apps.movimientos.urls')),
    path('reportes/', include('apps.reportes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
