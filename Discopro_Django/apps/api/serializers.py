from rest_framework import serializers
from apps.usuarios.models import Usuario, Departamento
from apps.motoristas.models import Motorista, Moto
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
    moto = serializers.SerializerMethodField()
    sucursal = serializers.SerializerMethodField()

    class Meta:
        model = Motorista
        fields = ['id', 'usuario', 'licencia', 'tipo_licencia', 'vigencia_licencia',
                  'moto', 'sucursal', 'region', 'provincia', 'comuna', 'direccion', 'estado',
                  'movimientos_completados', 'calificacion_promedio', 'activo']

    def get_moto(self, obj):
        moto = obj.moto_actual
        return MotoSerializer(moto).data if moto else None

    def get_sucursal(self, obj):
        sucursal = obj.sucursal_actual
        return SucursalSerializer(sucursal).data if sucursal else None


class MotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moto
        fields = ['id', 'placa', 'marca', 'modelo', 'año', 'color', 'estado', 'activo']


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['id', 'nombre', 'region', 'provincia', 'comuna', 'direccion', 'telefono', 'encargado_nombre', 'activo']


class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = [
            'id', 'numero_despacho', 'sucursal', 'direccion_origen', 'direccion_destino',
            'motorista', 'estado', 'creado_en', 'actualizado_en',
        ]


class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = ['id', 'titulo', 'tipo', 'fecha_inicio', 'fecha_fin', 'creado_en']
