from django.contrib import admin
from .models import AsignacionOperativa, Motorista, Moto, Sucursal


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region', 'provincia', 'comuna', 'direccion', 'telefono', 'encargado_nombre', 'activo', 'creado_en')
    list_filter = ('activo', 'region', 'provincia', 'comuna', 'creado_en')
    search_fields = ('nombre', 'region', 'provincia', 'comuna', 'direccion', 'telefono', 'encargado_nombre')
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'region', 'provincia', 'comuna', 'direccion', 'telefono')
        }),
        ('Referencia', {
            'fields': ('encargado_nombre', 'activo')
        }),
        ('Metadata', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('creado_en', 'actualizado_en')


@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'año', 'estado', 'activo', 'creado_en')
    list_filter = ('estado', 'activo', 'creado_en', 'año')
    search_fields = ('placa', 'marca', 'modelo', 'color')
    fieldsets = (
        ('Información del Vehículo', {
            'fields': ('placa', 'marca', 'modelo', 'año', 'color')
        }),
        ('Estado operacional', {
            'fields': ('estado',)
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


class AsignacionOperativaInline(admin.TabularInline):
    model = AsignacionOperativa
    extra = 0
    readonly_fields = ('creado_en',)
    fields = ('moto', 'sucursal', 'activa', 'observaciones', 'creado_en')


@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'licencia', 'region', 'provincia', 'comuna', 'estado', 'movimientos_completados', 'creado_en')
    list_filter = ('estado', 'activo', 'creado_en', 'tipo_licencia', 'region', 'provincia', 'comuna')
    search_fields = ('usuario__user__username', 'usuario__rut', 'licencia')
    inlines = [AsignacionOperativaInline]
    fieldsets = (
        ('Información del Motorista', {
            'fields': ('usuario',)
        }),
        ('Datos de Licencia', {
            'fields': ('licencia', 'tipo_licencia', 'vigencia_licencia')
        }),
        ('Ubicación', {
            'fields': ('region', 'provincia', 'comuna', 'direccion', 'ubicacion_actual', 'latitud', 'longitud')
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


@admin.register(AsignacionOperativa)
class AsignacionOperativaAdmin(admin.ModelAdmin):
    list_display = ('motorista', 'sucursal', 'moto', 'activa', 'creado_en')
    list_filter = ('activa', 'creado_en')
    search_fields = ('motorista__usuario__user__username', 'sucursal__nombre', 'moto__placa')
