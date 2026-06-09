from rest_framework import serializers
from apps.usuarios.models import Usuario, Departamento
from apps.motoristas.models import Motorista
from apps.movimientos.models import Movimiento
from apps.motoristas.models import Sucursal
from apps.reportes.models import Reporte


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'tipo', 'descripcion']


class UsuarioSerializer(serializers.ModelSerializer):
    departamento = DepartamentoSerializer()
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'rut', 'telefono', 'rol', 'departamento', 'estado', 'creado_en', 'first_name', 'last_name']


class MotoristaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    
    class Meta:
        model = Motorista
        fields = ['id', 'usuario', 'licencia', 'tipo_licencia', 'vigencia_licencia',
                  'vehiculo_placa', 'marca_vehiculo', 'modelo_vehiculo', 'estado',
                  'movimientos_completados', 'calificacion_promedio', 'activo']


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['id', 'nombre', 'direccion', 'ciudad', 'telefono', 'activo']


class MovimientoSerializer(serializers.ModelSerializer):
    motorista = MotoristaSerializer()
    sucursal = SucursalSerializer()
    
    class Meta:
        model = Movimiento
        fields = ['id', 'numero_despacho', 'motorista', 'sucursal', 'tipo_movimiento',
                  'estado', 'descripcion', 'fecha_programada', 'fecha_inicio',
                  'fecha_cierre', 'estado', 'calificacion', 'comentarios', 'creado_en']


class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = ['id', 'titulo', 'tipo', 'fecha_inicio', 'fecha_fin', 'creado_en']
