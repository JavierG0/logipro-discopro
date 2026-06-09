from django.db import models
from apps.usuarios.models import Usuario


class Sucursal(models.Model):
    """Modelo para las sucursales de la empresa"""
    nombre = models.CharField(max_length=100, unique=True)
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True)
    encargado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='sucursales_encargadas')
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sucursal_flota'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Moto(models.Model):
    """Modelo para los vehículos (motos)"""
    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.IntegerField()
    color = models.CharField(max_length=30, blank=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT, related_name='motos')
    estado = models.CharField(
        max_length=20,
        choices=[
            ('disponible', 'Disponible'),
            ('en_mantenimiento', 'En Mantenimiento'),
            ('dañada', 'Dañada'),
            ('retirada', 'Retirada'),
        ],
        default='disponible'
    )
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'moto'
        verbose_name = 'Moto'
        verbose_name_plural = 'Motos'
        ordering = ['placa']
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"


class Motorista(models.Model):
    """Modelo para los motoristas"""
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('en_ruta', 'En Ruta'),
        ('inactivo', 'Inactivo'),
        ('bloqueado', 'Bloqueado'),
    ]
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='motorista')
    licencia = models.CharField(max_length=20, unique=True)
    tipo_licencia = models.CharField(max_length=5, default='B')
    vigencia_licencia = models.DateField()
    moto = models.ForeignKey(Moto, on_delete=models.SET_NULL, null=True, blank=True, related_name='motoristas')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT, null=True, blank=True, related_name='motoristas')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')
    ubicacion_actual = models.CharField(max_length=255, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    movimientos_completados = models.IntegerField(default=0)
    calificacion_promedio = models.FloatField(default=5.0)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'motorista'
        verbose_name = 'Motorista'
        verbose_name_plural = 'Motoristas'
        ordering = ['-creado_en']
    
    def __str__(self):
        moto_info = f" - {self.moto.placa}" if self.moto else ""
        return f"{self.usuario.user.get_full_name()}{moto_info}"
