from django.urls import path
from . import views

app_name = 'movimientos'

urlpatterns = [
    path('', views.lista_movimientos, name='lista'),
    path('<int:pk>/', views.detalle_movimiento, name='detalle'),
    path('crear/', views.crear_movimiento, name='crear'),
    path('<int:pk>/editar/', views.editar_movimiento, name='editar'),
    path('<int:pk>/completar/', views.completar_movimiento, name='completar'),
    path('exportar/', views.exportar_movimientos, name='exportar'),
]
