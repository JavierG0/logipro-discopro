from django.db import models
from django.contrib.auth.models import User

class Departamento(models.Model):
    TIPOS_DEPARTAMENTO = [
        ('admin', 'Administrador'),
        ('despacho', 'Despacho'),
        ('operacion', 'Operación'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=50, choices=TIPOS_DEPARTAMENTO)
    descripcion = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
    
    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    ROLES = [
        ('administrador', 'Administrador'),
        ('despachador', 'Despachador'),
        ('operador', 'Operador'),
        ('motorista', 'Motorista'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario_profile')
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='motorista')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.BooleanField(default=True)
    foto_perfil = models.ImageField(upload_to='usuarios/fotos/', null=True, blank=True)
    ultimo_login = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-creado_en']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.rut})"
