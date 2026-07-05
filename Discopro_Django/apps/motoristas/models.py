from django.db import models
from django.db.models import Q
from apps.usuarios.models import Usuario


class Sucursal(models.Model):
    """Punto de origen (farmacia cliente) — solo datos operativos, sin acceso al sistema."""
    nombre = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=100, default='')
    provincia = models.CharField(max_length=100, default='')
    comuna = models.CharField(max_length=100, default='')
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    encargado_nombre = models.CharField(max_length=120, blank=True, default='')
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sucursal_flota'
        verbose_name = 'Farmacia origen'
        verbose_name_plural = 'Farmacias origen'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def direccion_completa(self):
        partes = [p for p in (self.direccion, self.comuna, self.provincia, self.region) if p]
        return ', '.join(partes)


class Moto(models.Model):
    """Vehículos de la flota logística."""
    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.IntegerField()
    color = models.CharField(max_length=30, blank=True)
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
    """Datos operativos del conductor. Credenciales en auth.User + Usuario."""
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
    region = models.CharField(max_length=100, default='')
    provincia = models.CharField(max_length=100, default='')
    comuna = models.CharField(max_length=100, default='')
    direccion = models.CharField(max_length=255, blank=True, default='')
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
        moto = self.moto_actual
        moto_info = f" - {moto.placa}" if moto else ""
        return f"{self.usuario.user.get_full_name()}{moto_info}"

    @property
    def moto_actual(self):
        asignacion = self.asignaciones.filter(activa=True).select_related('moto').first()
        return asignacion.moto if asignacion else None

    @property
    def sucursal_actual(self):
        asignacion = self.asignaciones.filter(activa=True).select_related('sucursal').first()
        return asignacion.sucursal if asignacion else None

    # Compatibilidad con código existente
    @property
    def moto(self):
        return self.moto_actual

    @property
    def sucursal(self):
        return self.sucursal_actual


class AsignacionOperativa(models.Model):
    """Tabla intermedia: asignación de moto y farmacia origen a un motorista."""
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE, related_name='asignaciones')
    moto = models.ForeignKey(Moto, on_delete=models.SET_NULL, null=True, blank=True, related_name='asignaciones')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT, related_name='asignaciones')
    activa = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, default='')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asignacion_operativa'
        verbose_name = 'Asignación operativa'
        verbose_name_plural = 'Asignaciones operativas'
        ordering = ['-creado_en']
        constraints = [
            models.UniqueConstraint(
                fields=['motorista'],
                condition=Q(activa=True),
                name='unique_asignacion_activa_por_motorista',
            ),
        ]

    def __str__(self):
        moto = self.moto.placa if self.moto else 'Sin moto'
        return f"{self.motorista} → {self.sucursal.nombre} / {moto}"


def sincronizar_asignacion(motorista, moto, sucursal, observaciones=''):
    """Registra o actualiza la asignación activa de un motorista."""
    if sucursal is None:
        return None
    AsignacionOperativa.objects.filter(motorista=motorista, activa=True).update(activa=False)
    return AsignacionOperativa.objects.create(
        motorista=motorista,
        moto=moto,
        sucursal=sucursal,
        activa=True,
        observaciones=observaciones,
    )
