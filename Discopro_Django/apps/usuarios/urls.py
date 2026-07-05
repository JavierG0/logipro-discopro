from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('cambiar-contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),
    path('administracion/', views.lista_usuarios_sistema, name='lista_sistema'),
    path('administracion/crear/', views.crear_usuario_sistema, name='crear_sistema'),
    path('administracion/<int:pk>/editar/', views.editar_usuario_sistema, name='editar_sistema'),
]
