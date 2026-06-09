from django.contrib import admin
from .models import Motorista, Moto, Sucursal


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'direccion', 'telefono', 'encargado', 'activo', 'creado_en')
    list_filter = ('activo', 'ciudad', 'creado_en')
    search_fields = ('nombre', 'ciudad', 'direccion', 'telefono')
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'ciudad', 'direccion', 'telefono')
        }),
        ('Gestión', {
            'fields': ('encargado', 'activo')
        }),
        ('Metadata', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('creado_en', 'actualizado_en')


@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'año', 'sucursal', 'estado', 'activo', 'creado_en')
    list_filter = ('estado', 'activo', 'sucursal', 'creado_en', 'año')
    search_fields = ('placa', 'marca', 'modelo', 'color')
    fieldsets = (
        ('Información del Vehículo', {
            'fields': ('placa', 'marca', 'modelo', 'año', 'color')
        }),
        ('Asignación', {
            'fields': ('sucursal', 'estado')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Metadata', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('creado_en', 'actualizado_en')


@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'licencia', 'moto', 'sucursal', 'estado', 'movimientos_completados', 'creado_en')
    list_filter = ('estado', 'activo', 'creado_en', 'tipo_licencia', 'sucursal')
    search_fields = ('usuario__user__username', 'usuario__rut', 'licencia', 'moto__placa')
    fieldsets = (
        ('Información del Motorista', {
            'fields': ('usuario',)
        }),
        ('Datos de Licencia', {
            'fields': ('licencia', 'tipo_licencia', 'vigencia_licencia')
        }),
        ('Asignación de Recursos', {
            'fields': ('moto', 'sucursal')
        }),
        ('Ubicación', {
            'fields': ('ubicacion_actual', 'latitud', 'longitud')
        }),
        ('Estado', {
            'fields': ('estado', 'activo')
        }),
        ('Estadísticas', {
            'fields': ('movimientos_completados', 'calificacion_promedio'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('creado_en', 'actualizado_en', 'movimientos_completados')
