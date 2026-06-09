from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartamentoViewSet, UsuarioViewSet, MotoristaViewSet,
    SucursalViewSet, MovimientoViewSet, ReporteViewSet
)

router = DefaultRouter()
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'motoristas', MotoristaViewSet, basename='motorista')
router.register(r'sucursales', SucursalViewSet, basename='sucursal')
router.register(r'movimientos', MovimientoViewSet, basename='movimiento')
router.register(r'reportes', ReporteViewSet, basename='reporte')

urlpatterns = [
    path('', include(router.urls)),
]
