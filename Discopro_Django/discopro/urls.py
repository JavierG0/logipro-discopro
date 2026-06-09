"""

URL configuration for discopro project.

"""

from django.contrib import admin

from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static

from django.views.generic import RedirectView



from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.utils import timezone

from django.utils.dateparse import parse_datetime

from apps.movimientos.models import Movimiento

from apps.movimientos.utils import filtrar_movimientos

from apps.motoristas.models import Motorista, Sucursal, Moto





def _crear_movimiento_desde_post(request):

    numero_despacho = request.POST.get('numero_despacho', '').strip()

    motorista_id = request.POST.get('motorista')

    moto_id = request.POST.get('moto')

    sucursal_id = request.POST.get('sucursal')

    tipo_movimiento = request.POST.get('tipo_movimiento')

    descripcion = request.POST.get('descripcion', '').strip()

    observaciones = request.POST.get('observaciones', '').strip()

    fecha_programada_raw = request.POST.get('fecha_programada')

    destinatario_nombre = request.POST.get('destinatario_nombre', '').strip()

    destinatario_rut = request.POST.get('destinatario_rut', '').strip()

    destinatario_telefono = request.POST.get('destinatario_telefono', '').strip()

    destinatario_direccion = request.POST.get('destinatario_direccion', '').strip()

    destinatario_comuna = request.POST.get('destinatario_comuna', '').strip()

    destinatario_region = request.POST.get('destinatario_region', '').strip()



    campos_obligatorios = [

        numero_despacho, tipo_movimiento, descripcion, fecha_programada_raw,

        sucursal_id, motorista_id, moto_id, destinatario_nombre, destinatario_rut,

        destinatario_telefono, destinatario_direccion, destinatario_comuna, destinatario_region,

    ]

    if not all(campos_obligatorios):

        messages.error(request, 'Complete todos los campos obligatorios.')

        return False

    if Movimiento.objects.filter(numero_despacho=numero_despacho).exists():

        messages.error(request, 'El número de despacho ya existe.')

        return False



    fecha_programada = parse_datetime(fecha_programada_raw)

    if fecha_programada is None:

        messages.error(request, 'La fecha programada no es válida.')

        return False

    if timezone.is_naive(fecha_programada):

        fecha_programada = timezone.make_aware(fecha_programada)



    motorista = get_object_or_404(Motorista, pk=motorista_id)

    moto = get_object_or_404(Moto, pk=moto_id, activo=True)

    sucursal = get_object_or_404(Sucursal, pk=sucursal_id, activo=True)

    motorista.moto = moto

    motorista.save(update_fields=['moto'])

    Movimiento.objects.create(

        numero_despacho=numero_despacho,

        motorista=motorista,

        sucursal=sucursal,

        tipo_movimiento=tipo_movimiento,

        descripcion=descripcion,

        destinatario_nombre=destinatario_nombre,

        destinatario_rut=destinatario_rut,

        destinatario_telefono=destinatario_telefono,

        destinatario_direccion=destinatario_direccion,

        destinatario_comuna=destinatario_comuna,

        destinatario_region=destinatario_region,

        observaciones=observaciones,

        fecha_programada=fecha_programada,

    )

    messages.success(request, 'Movimiento registrado exitosamente.')

    return True





@login_required(login_url='usuarios:login')

def home(request):

    motoristas = Motorista.objects.filter(activo=True).select_related('usuario__user', 'moto')

    sucursales = Sucursal.objects.filter(activo=True)

    motos = Moto.objects.filter(activo=True).select_related('sucursal')



    movimientos = Movimiento.objects.select_related(

        'motorista__usuario__user',

        'motorista__moto',

        'sucursal',

    ).order_by('-fecha_programada')

    movimientos = filtrar_movimientos(movimientos, request.GET)

    if not any(request.GET.get(k) for k in ('q_despacho', 'q_motorista', 'q_moto', 'q_fecha', 'q_destinatario')):

        movimientos = movimientos[:20]



    stats = {

        'completados': Movimiento.objects.filter(estado='completado').count(),

        'transito': Movimiento.objects.filter(estado='en_transito').count(),

        'disponibles': Motorista.objects.filter(estado='disponible', activo=True).count(),

    }



    if request.method == 'POST':

        if _crear_movimiento_desde_post(request):

            return redirect('home')



    return render(request, 'dashboard.html', {

        'motoristas': motoristas,

        'motos': motos,

        'sucursales': sucursales,

        'movimientos': movimientos,

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

    path('motoristas/sucursales/', RedirectView.as_view(pattern_name='farmacia:lista', permanent=True)),

    path('motoristas/', include('apps.motoristas.urls')),

    path('movimientos/', include('apps.movimientos.urls')),

    path('reportes/', include('apps.reportes.urls')),

]



if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


