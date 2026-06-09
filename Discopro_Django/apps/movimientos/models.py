from django.db import models
from apps.motoristas.models import Motorista, Sucursal


class Movimiento(models.Model):
    TIPOS_MOVIMIENTO = [
        ('entrega', 'Entrega de Producto'),
        ('retiro', 'Retiro de Receta'),
        ('reemplazo', 'Reemplazo'),
    ]
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('asignado', 'Asignado'),
        ('en_transito', 'En Transito'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    numero_despacho = models.CharField(max_length=50, unique=True)
    motorista = models.ForeignKey(Motorista, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPOS_MOVIMIENTO)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    descripcion = models.TextField()
    destinatario_nombre = models.CharField(max_length=200, blank=True, default='')
    destinatario_rut = models.CharField(max_length=12, blank=True, default='')
    destinatario_telefono = models.CharField(max_length=15, blank=True, default='')
    destinatario_direccion = models.CharField(max_length=255, blank=True, default='')
    destinatario_comuna = models.CharField(max_length=100, blank=True, default='')
    destinatario_region = models.CharField(max_length=100, blank=True, default='')
    observaciones = models.TextField(blank=True)
    fecha_programada = models.DateTimeField()
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    hora_estimada_entrega = models.TimeField(null=True, blank=True)
    distancia_km = models.FloatField(null=True, blank=True)
    duracion_minutos = models.IntegerField(null=True, blank=True)
    firma_confirmacion = models.ImageField(upload_to='movimientos/firmas/', null=True, blank=True)
    calificacion = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    comentarios = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'movimiento'
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['-fecha_programada']
        indexes = [
            models.Index(fields=['numero_despacho']),
            models.Index(fields=['motorista', 'estado']),
            models.Index(fields=['fecha_programada']),
        ]
    
    def __str__(self):
        return f"{self.numero_despacho} - {self.get_estado_display()}"
