from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.usuarios.models import Usuario, Departamento
from apps.motoristas.models import Motorista
from apps.movimientos.models import Movimiento
from apps.motoristas.models import Sucursal
from apps.reportes.models import Reporte
from .serializers import (
    UsuarioSerializer, MotoristaSerializer, MovimientoSerializer,
    SucursalSerializer, ReporteSerializer, DepartamentoSerializer
)


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.IsAuthenticated]


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def mi_perfil(self, request):
        usuario = Usuario.objects.get(user=request.user)
        serializer = self.get_serializer(usuario)
        return Response(serializer.data)


class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.select_related('usuario__user').prefetch_related(
        'asignaciones__moto', 'asignaciones__sucursal',
    ).all()
    serializer_class = MotoristaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset


class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.filter(activo=True)
    serializer_class = SucursalSerializer
    permission_classes = [permissions.IsAuthenticated]


class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        numero_despacho = self.request.query_params.get('numero_despacho')
        if numero_despacho:
            queryset = queryset.filter(numero_despacho__icontains=numero_despacho)
        return queryset


class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
