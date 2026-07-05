from django.db import models
from apps.motoristas.models import Motorista, Sucursal


class Movimiento(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_ruta', 'En Ruta'),
        ('entregado', 'Entregado'),
        ('incidencia', 'Incidencia'),
    ]

    TIPOS_INCIDENCIA = [
        ('direccion_incorrecta', 'Dirección incorrecta'),
        ('cliente_ausente', 'Cliente ausente'),
        ('problema_mecanico', 'Problema mecánico'),
        ('no_entregado', 'No fue posible entregar'),
        ('otro', 'Otro'),
    ]

    numero_despacho = models.CharField(max_length=50, unique=True)
    sucursal = models.ForeignKey(
        Sucursal, on_delete=models.PROTECT, null=True, blank=True,
        related_name='despachos', verbose_name='Farmacia origen',
    )
    direccion_origen = models.CharField(max_length=255, blank=True, default='')
    direccion_destino = models.CharField(max_length=255, default='')
    motorista = models.ForeignKey(Motorista, on_delete=models.SET_NULL, null=True, blank=True, related_name='despachos')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    tipo_incidencia = models.CharField(max_length=30, choices=TIPOS_INCIDENCIA, blank=True, default='')
    comentario_incidencia = models.TextField(blank=True, default='')
    entregado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'movimiento'
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['-creado_en']
        indexes = [
            models.Index(fields=['numero_despacho']),
            models.Index(fields=['motorista', 'estado']),
        ]

    def __str__(self):
        return self.numero_despacho

    def save(self, *args, **kwargs):
        if self.sucursal_id and not self.direccion_origen:
            self.direccion_origen = self.sucursal.direccion_completa or self.sucursal.direccion
        super().save(*args, **kwargs)
