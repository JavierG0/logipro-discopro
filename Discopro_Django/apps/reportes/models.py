from django.db import models
from apps.usuarios.models import Usuario


class Reporte(models.Model):
    TIPOS_REPORTE = [
        ('movimientos', 'Reporte de Movimientos'),
        ('motoristas', 'Reporte de Motoristas'),
        ('ingresos', 'Reporte de Ingresos'),
        ('desempenio', 'Reporte de Desempeño'),
    ]
    
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=TIPOS_REPORTE)
    descripcion = models.TextField()
    usuario_creador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    archivo = models.FileField(upload_to='reportes/', null=True, blank=True)
    datos_json = models.JSONField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reporte'
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
        ordering = ['-creado_en']
    
    def __str__(self):
        return self.titulo
