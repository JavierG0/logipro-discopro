from django.contrib import admin
from .models import Movimiento


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('numero_despacho', 'tipo_movimiento', 'estado', 'motorista', 'sucursal', 'fecha_programada')
    list_filter = ('estado', 'tipo_movimiento', 'fecha_programada', 'sucursal')
    search_fields = ('numero_despacho', 'motorista__usuario__user__username')
    fieldsets = (
        ('Información General', {
            'fields': ('numero_despacho', 'tipo_movimiento', 'estado')
        }),
        ('Datos de Asignación', {
            'fields': ('motorista', 'sucursal', 'fecha_programada')
        }),
        ('Descripción', {
            'fields': ('descripcion', 'observaciones')
        }),
        ('Seguimiento', {
            'fields': ('fecha_inicio', 'fecha_cierre', 'hora_estimada_entrega', 'distancia_km', 'duracion_minutos')
        }),
        ('Confirmación', {
            'fields': ('firma_confirmacion', 'calificacion', 'comentarios')
        }),
        ('Metadata', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('creado_en', 'actualizado_en')
