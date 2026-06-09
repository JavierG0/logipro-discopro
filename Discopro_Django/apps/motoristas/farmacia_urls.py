from django.urls import path
from . import views

app_name = 'farmacia'

urlpatterns = [
    path('', views.lista_sucursales, name='lista'),
    path('crear/', views.crear_sucursal, name='crear'),
    path('<int:pk>/editar/', views.editar_sucursal, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_sucursal, name='eliminar'),
]
