from django.urls import path
from . import views

app_name = 'motoristas'

urlpatterns = [
    # Motos
    path('motos/', views.lista_motos, name='lista_motos'),
    path('motos/crear/', views.crear_moto, name='crear_moto'),
    path('motos/<int:pk>/editar/', views.editar_moto, name='editar_moto'),
    path('motos/<int:pk>/eliminar/', views.eliminar_moto, name='eliminar_moto'),
    
    # Motoristas
    path('', views.lista_motoristas, name='lista'),
    path('<int:pk>/', views.detalle_motorista, name='detalle'),
    path('crear/', views.crear_motorista, name='crear'),
    path('<int:pk>/editar/', views.editar_motorista, name='editar'),
]
