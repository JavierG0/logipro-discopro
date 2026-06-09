from django.contrib import admin
from .models import Reporte


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'usuario_creador', 'fecha_inicio', 'fecha_fin', 'creado_en')
    list_filter = ('tipo', 'creado_en')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('creado_en', 'actualizado_en')
