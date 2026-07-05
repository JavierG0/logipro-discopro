from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Prefetch
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from apps.usuarios.permissions import administrador_requerido
from .geografia import comunas, provincias
from .models import Motorista, Moto, Sucursal, AsignacionOperativa
from .forms import MotoristaForm, MotoristaCreateForm, MotoForm, SucursalForm


MOTORISTA_PREFETCH = Prefetch(
    'asignaciones',
    queryset=AsignacionOperativa.objects.filter(activa=True).select_related('moto', 'sucursal'),
)


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
            Q(region__icontains=busqueda) |
            Q(provincia__icontains=busqueda) |
            Q(comuna__icontains=busqueda) |
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


@require_GET
@login_required(login_url='usuarios:login')
def api_provincias(request):
    region = request.GET.get('region', '')
    return JsonResponse({'provincias': provincias(region)})


@require_GET
@login_required(login_url='usuarios:login')
def api_comunas(request):
    region = request.GET.get('region', '')
    provincia = request.GET.get('provincia', '')
    return JsonResponse({'comunas': comunas(region, provincia)})


@require_GET
@login_required(login_url='usuarios:login')
def api_farmacia_motoristas(request, pk):
    """Motoristas asignados a una farmacia de origen (para registro de despachos)."""
    sucursal = get_object_or_404(Sucursal, pk=pk, activo=True)
    motoristas = Motorista.objects.filter(
        activo=True,
        asignaciones__sucursal=sucursal,
        asignaciones__activa=True,
    ).select_related('usuario__user').prefetch_related(MOTORISTA_PREFETCH).distinct()
    data = []
    for m in motoristas:
        moto = m.moto_actual
        data.append({
            'id': m.id,
            'nombre': m.usuario.user.get_full_name(),
            'moto': moto.placa if moto else None,
        })
    return JsonResponse({'motoristas': data})


@require_GET
@login_required(login_url='usuarios:login')
def api_farmacia_direccion(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk, activo=True)
    return JsonResponse({
        'direccion': sucursal.direccion_completa,
        'direccion_calle': sucursal.direccion,
        'nombre': sucursal.nombre,
    })


# ==================== MOTOS ====================

@login_required(login_url='usuarios:login')
@administrador_requerido
def lista_motos(request):
    """Listado de motos"""
    motos = Moto.objects.prefetch_related('asignaciones__motorista__usuario__user').all()
    
    estado = request.GET.get('estado')
    busqueda = request.GET.get('busqueda')
    
    if estado:
        motos = motos.filter(estado=estado)
    
    if busqueda:
        motos = motos.filter(
            Q(placa__icontains=busqueda) |
            Q(marca__icontains=busqueda) |
            Q(modelo__icontains=busqueda)
        )
    
    return render(request, 'motos.html', {
        'motos': motos,
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
    motoristas = Motorista.objects.select_related('usuario__user').prefetch_related(MOTORISTA_PREFETCH).all()
    
    # Filtros
    estado = request.GET.get('estado')
    sucursal = request.GET.get('sucursal')
    busqueda = request.GET.get('busqueda')
    
    if estado:
        motoristas = motoristas.filter(estado=estado)
    
    if sucursal:
        motoristas = motoristas.filter(asignaciones__sucursal_id=sucursal, asignaciones__activa=True)
    
    if busqueda:
        motoristas = motoristas.filter(
            Q(usuario__user__first_name__icontains=busqueda) |
            Q(usuario__user__last_name__icontains=busqueda) |
            Q(usuario__rut__icontains=busqueda) |
            Q(asignaciones__moto__placa__icontains=busqueda) |
            Q(region__icontains=busqueda) |
            Q(provincia__icontains=busqueda) |
            Q(comuna__icontains=busqueda)
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
    motorista = get_object_or_404(
        Motorista.objects.select_related('usuario__user').prefetch_related(MOTORISTA_PREFETCH),
        pk=pk,
    )
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
