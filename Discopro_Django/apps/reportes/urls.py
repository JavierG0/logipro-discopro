from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.lista_reportes, name='lista'),
    path('<int:pk>/', views.detalle_reporte, name='detalle'),
    path('generar/', views.generar_reporte, name='generar'),
    path('<int:pk>/descargar/', views.descargar_reporte, name='descargar'),
]
