from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Usuario

@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vista de login de usuarios"""
    # Si el usuario ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Actualizar último login
            usuario = Usuario.objects.get(user=user)
            from django.utils import timezone
            usuario.ultimo_login = timezone.now()
            usuario.save()
            messages.success(request, f'¡Bienvenido {user.first_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'login.html')


@login_required(login_url='usuarios:login')
def logout_view(request):
    """Vista de cierre de sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('usuarios:login')


@login_required(login_url='usuarios:login')
def perfil_view(request):
    """Vista del perfil de usuario"""
    try:
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        usuario = None
    
    return render(request, 'perfil.html', {'usuario': usuario})


@login_required(login_url='usuarios:login')
@require_http_methods(["GET", "POST"])
def cambiar_contraseña(request):
    """Vista para cambiar contraseña"""
    if request.method == 'POST':
        contraseña_actual = request.POST.get('contraseña_actual')
        contraseña_nueva = request.POST.get('contraseña_nueva')
        confirmar_contraseña = request.POST.get('confirmar_contraseña')
        
        if not request.user.check_password(contraseña_actual):
            messages.error(request, 'Contraseña actual incorrecta')
            return redirect('usuarios:cambiar_contraseña')
        
        if contraseña_nueva != confirmar_contraseña:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('usuarios:cambiar_contraseña')
        
        request.user.set_password(contraseña_nueva)
        request.user.save()
        messages.success(request, 'Contraseña cambiada correctamente')
        return redirect('usuarios:perfil')
    
    return render(request, 'cambiar_contraseña.html')
