from django.contrib import admin
from .models import Usuario, Departamento


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'creado_en')
    list_filter = ('tipo', 'creado_en')
    search_fields = ('nombre', 'descripcion')


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'rol', 'departamento', 'estado', 'creado_en')
    list_filter = ('rol', 'estado', 'departamento', 'creado_en')
    search_fields = ('user__username', 'rut', 'user__email')
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user', 'rut', 'telefono')
        }),
        ('Datos de Acceso', {
            'fields': ('rol', 'departamento', 'estado')
        }),
        ('Multimedia', {
            'fields': ('foto_perfil',)
        }),
        ('Metadata', {
            'fields': ('ultimo_login', 'creado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('creado_en', 'actualizado_en', 'ultimo_login')
