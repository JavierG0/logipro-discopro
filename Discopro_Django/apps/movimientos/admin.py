from django.contrib import admin
from .models import Movimiento


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('numero_despacho', 'direccion_destino', 'motorista', 'sucursal', 'estado', 'creado_en')
    list_filter = ('estado', 'sucursal', 'creado_en')
    search_fields = ('numero_despacho', 'direccion_destino', 'motorista__usuario__user__first_name', 'motorista__usuario__user__last_name')
    fieldsets = (
        ('Información General', {
            'fields': ('numero_despacho', 'direccion_destino', 'motorista', 'sucursal', 'estado')
        }),
        ('Incidencia', {
            'fields': ('tipo_incidencia', 'comentario_incidencia')
        }),
        ('Entrega', {
            'fields': ('entregado_en',)
        }),
        ('Metadata', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('creado_en', 'actualizado_en')
