from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from .forms import UsuarioSistemaForm
from .models import Usuario
from .permissions import administrador_sistema_requerido


def redireccion_por_rol(user):
    try:
        if user.usuario_profile.rol == 'motorista':
            return 'portal_motorista:inicio'
    except Usuario.DoesNotExist:
        pass
    return 'home'


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect(redireccion_por_rol(request.user))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                usuario = Usuario.objects.get(user=user)
                from django.utils import timezone
                usuario.ultimo_login = timezone.now()
                usuario.save()
            except Usuario.DoesNotExist:
                pass
            messages.success(request, f'¡Bienvenido {user.first_name}!')
            return redirect(redireccion_por_rol(user))
        messages.error(request, 'Credenciales inválidas')

    return render(request, 'login.html')


@login_required(login_url='usuarios:login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('usuarios:login')


@login_required(login_url='usuarios:login')
def perfil_view(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        usuario = None
    return render(request, 'perfil.html', {'usuario': usuario})


@login_required(login_url='usuarios:login')
@require_http_methods(["GET", "POST"])
def cambiar_contraseña(request):
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


@login_required(login_url='usuarios:login')
@administrador_sistema_requerido
def lista_usuarios_sistema(request):
    usuarios = Usuario.objects.select_related('user', 'departamento').exclude(rol='motorista')
    q = request.GET.get('q', '').strip()
    if q:
        usuarios = usuarios.filter(
            Q(user__username__icontains=q)
            | Q(user__first_name__icontains=q)
            | Q(user__last_name__icontains=q)
            | Q(rut__icontains=q)
        )
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios, 'q': q})


@login_required(login_url='usuarios:login')
@administrador_sistema_requerido
def crear_usuario_sistema(request):
    if request.method == 'POST':
        form = UsuarioSistemaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario del sistema creado correctamente.')
            return redirect('usuarios:lista_sistema')
    else:
        form = UsuarioSistemaForm()
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'titulo': 'Crear usuario del sistema'})


@login_required(login_url='usuarios:login')
@administrador_sistema_requerido
def editar_usuario_sistema(request, pk):
    usuario = get_object_or_404(Usuario.objects.select_related('user'), pk=pk)
    if request.method == 'POST':
        form = UsuarioSistemaForm(request.POST, instance=usuario, usuario_instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('usuarios:lista_sistema')
    else:
        form = UsuarioSistemaForm(instance=usuario, usuario_instance=usuario)
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'titulo': 'Editar usuario del sistema', 'usuario': usuario})
