from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from apps.usuarios.permissions import administrador_requerido
from .models import Motorista, Moto, Sucursal
from .forms import MotoristaForm, MotoristaCreateForm, MotoForm, SucursalForm


# ==================== SUCURSALES ====================

@login_required(login_url='usuarios:login')
@administrador_requerido
def lista_sucursales(request):
    """Listado de sucursales"""
    sucursales = Sucursal.objects.all()
    
    busqueda = request.GET.get('busqueda')
    if busqueda:
        sucursales = sucursales.filter(
            Q(nombre__icontains=busqueda) |
            Q(ciudad__icontains=busqueda) |
            Q(direccion__icontains=busqueda)
        )
    
    return render(request, 'sucursales.html', {
        'sucursales': sucursales
    })


@login_required(login_url='usuarios:login')
@administrador_requerido
def crear_sucursal(request):
    """Crear una nueva sucursal"""
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sucursal creada exitosamente.')
            return redirect('farmacia:lista')
    else:
        form = SucursalForm()
    
    return render(request, 'sucursal_crear.html', {'form': form})


@login_required(login_url='usuarios:login')
@administrador_requerido
def editar_sucursal(request, pk):
    """Editar sucursal"""
    sucursal = get_object_or_404(Sucursal, pk=pk)
    
    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sucursal actualizada exitosamente.')
            return redirect('farmacia:lista')
    else:
        form = SucursalForm(instance=sucursal)
    
    return render(request, 'sucursal_editar.html', {
        'sucursal': sucursal,
        'form': form
    })


@login_required(login_url='usuarios:login')
@administrador_requerido
def eliminar_sucursal(request, pk):
    """Eliminar sucursal"""
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        sucursal.delete()
        messages.success(request, 'Sucursal eliminada exitosamente.')
        return redirect('farmacia:lista')
    
    return render(request, 'sucursal_eliminar.html', {'sucursal': sucursal})


# ==================== MOTOS ====================

@login_required(login_url='usuarios:login')
@administrador_requerido
def lista_motos(request):
    """Listado de motos"""
    motos = Moto.objects.select_related('sucursal').all()
    
    estado = request.GET.get('estado')
    sucursal = request.GET.get('sucursal')
    busqueda = request.GET.get('busqueda')
    
    if estado:
        motos = motos.filter(estado=estado)
    
    if sucursal:
        motos = motos.filter(sucursal_id=sucursal)
    
    if busqueda:
        motos = motos.filter(
            Q(placa__icontains=busqueda) |
            Q(marca__icontains=busqueda) |
            Q(modelo__icontains=busqueda)
        )
    
    sucursales = Sucursal.objects.all()
    
    return render(request, 'motos.html', {
        'motos': motos,
        'sucursales': sucursales,
        'estados': Moto._meta.get_field('estado').choices
    })


@login_required(login_url='usuarios:login')
@administrador_requerido
def crear_moto(request):
    """Crear una nueva moto"""
    if request.method == 'POST':
        form = MotoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Moto creada exitosamente.')
            return redirect('motoristas:lista_motos')
    else:
        form = MotoForm()
    
    return render(request, 'moto_crear.html', {'form': form})


@login_required(login_url='usuarios:login')
@administrador_requerido
def editar_moto(request, pk):
    """Editar moto"""
    moto = get_object_or_404(Moto, pk=pk)
    
    if request.method == 'POST':
        form = MotoForm(request.POST, instance=moto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Moto actualizada exitosamente.')
            return redirect('motoristas:lista_motos')
    else:
        form = MotoForm(instance=moto)
    
    return render(request, 'moto_editar.html', {
        'moto': moto,
        'form': form
    })


@login_required(login_url='usuarios:login')
@administrador_requerido
def eliminar_moto(request, pk):
    """Eliminar moto"""
    moto = get_object_or_404(Moto, pk=pk)
    if request.method == 'POST':
        moto.delete()
        messages.success(request, 'Moto eliminada exitosamente.')
        return redirect('motoristas:lista_motos')
    
    return render(request, 'moto_eliminar.html', {'moto': moto})


# ==================== MOTORISTAS ====================

@login_required(login_url='usuarios:login')
@administrador_requerido
def lista_motoristas(request):
    """Listado de motoristas"""
    motoristas = Motorista.objects.select_related('usuario__user', 'moto', 'sucursal').all()
    
    # Filtros
    estado = request.GET.get('estado')
    sucursal = request.GET.get('sucursal')
    busqueda = request.GET.get('busqueda')
    
    if estado:
        motoristas = motoristas.filter(estado=estado)
    
    if sucursal:
        motoristas = motoristas.filter(sucursal_id=sucursal)
    
    if busqueda:
        motoristas = motoristas.filter(
            Q(usuario__user__first_name__icontains=busqueda) |
            Q(usuario__user__last_name__icontains=busqueda) |
            Q(usuario__rut__icontains=busqueda) |
            Q(moto__placa__icontains=busqueda)
        )
    
    sucursales = Sucursal.objects.all()
    
    return render(request, 'motoristas.html', {
        'motoristas': motoristas,
        'sucursales': sucursales,
        'estados': Motorista.ESTADOS
    })


@login_required(login_url='usuarios:login')
@administrador_requerido
def detalle_motorista(request, pk):
    """Detalle de un motorista"""
    motorista = get_object_or_404(Motorista.objects.select_related('usuario__user', 'moto', 'sucursal'), pk=pk)
    return render(request, 'motorista_detalle.html', {'motorista': motorista})


@login_required(login_url='usuarios:login')
@administrador_requerido
def crear_motorista(request):
    """Crear un nuevo motorista"""
    if request.method == 'POST':
        form = MotoristaCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Motorista creado exitosamente.')
            return redirect('motoristas:lista')
    else:
        form = MotoristaCreateForm()
    
    return render(request, 'motorista_crear.html', {'form': form})


@login_required(login_url='usuarios:login')
@administrador_requerido
def editar_motorista(request, pk):
    """Editar motorista"""
    motorista = get_object_or_404(Motorista, pk=pk)
    
    if request.method == 'POST':
        form = MotoristaForm(request.POST, instance=motorista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Motorista actualizado exitosamente.')
            return redirect('motoristas:detalle', pk=motorista.pk)
    else:
        form = MotoristaForm(instance=motorista)
    
    return render(request, 'motorista_editar.html', {
        'motorista': motorista,
        'form': form
    })
