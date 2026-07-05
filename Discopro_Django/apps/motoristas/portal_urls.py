from django.urls import path

from . import portal_views

app_name = 'portal_motorista'

urlpatterns = [
    path('', portal_views.inicio, name='inicio'),
    path('despachos/', portal_views.mis_despachos, name='mis_despachos'),
    path('despachos/<int:pk>/', portal_views.detalle_despacho, name='detalle'),
    path('despachos/<int:pk>/iniciar/', portal_views.iniciar_ruta, name='iniciar_ruta'),
    path('despachos/<int:pk>/entregado/', portal_views.marcar_entregado, name='entregado'),
    path('despachos/<int:pk>/incidencia/', portal_views.reportar_incidencia, name='incidencia'),
    path('perfil/', portal_views.perfil, name='perfil'),
    path('mi-moto/', portal_views.mi_moto, name='mi_moto'),
    path('historial/', portal_views.historial, name='historial'),
]
