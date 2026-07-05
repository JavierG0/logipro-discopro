import os
from datetime import date

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discopro.settings')
django.setup()

from django.contrib.auth.models import User

from apps.motoristas.models import Moto, Motorista, Sucursal, sincronizar_asignacion
from apps.movimientos.models import Movimiento
from apps.usuarios.models import Departamento, Usuario


PASSWORDS = {
    'admin_arica': 'AdminArica123',
    'despacho_arica': 'DespachoArica123',
    'operador_arica': 'OperadorArica123',
    'motorista_vega': 'Motorista123',
    'motorista_rojas': 'Motorista123',
    'motorista_condori': 'Motorista123',
    'motorista_mamani': 'Motorista123',
}


def crear_departamentos():
    departamentos = {
        'Administración': ('admin', 'Administración del sistema'),
        'Despacho': ('despacho', 'Gestión de flota y recursos'),
        'Operación': ('operacion', 'Registro de movimientos/despachos'),
    }
    creados = {}
    for nombre, (tipo, descripcion) in departamentos.items():
        departamento, _ = Departamento.objects.get_or_create(
            nombre=nombre,
            defaults={'tipo': tipo, 'descripcion': descripcion},
        )
        creados[nombre] = departamento
    return creados


def crear_usuario(username, password, first_name, last_name, email, rut, telefono, rol, departamento=None, is_staff=False, is_superuser=False):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'is_staff': is_staff,
            'is_superuser': is_superuser,
            'is_active': True,
        },
    )
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.is_active = True
    user.set_password(password)
    user.save()

    usuario = Usuario.objects.filter(user=user).first()
    if usuario is None:
        usuario = Usuario.objects.filter(rut=rut).first()
    if usuario is None:
        usuario = Usuario(user=user)
    elif usuario.user_id != user.id:
        usuario.user = user
    usuario.rut = rut
    usuario.telefono = telefono
    usuario.rol = rol
    usuario.departamento = departamento
    usuario.estado = True
    usuario.save()
    return usuario


def crear_farmacias():
    datos = [
        {
            'nombre': 'Cruz Verde Arica Centro',
            'region': 'Arica',
            'provincia': 'Arica',
            'comuna': 'Arica',
            'direccion': '21 de Mayo, sector centro',
        },
        {
            'nombre': 'Cruz Verde Mall Plaza Arica',
            'region': 'Arica',
            'provincia': 'Arica',
            'comuna': 'Arica',
            'direccion': 'Av. Diego Portales, sector Mall Plaza Arica',
        },
        {
            'nombre': 'Cruz Verde Santa María Arica',
            'region': 'Arica',
            'provincia': 'Arica',
            'comuna': 'Arica',
            'direccion': 'Av. Santa María, Arica',
        },
        {
            'nombre': 'Cruz Verde Putre Referencial',
            'region': 'Parinacota',
            'provincia': 'Parinacota',
            'comuna': 'Putre',
            'direccion': 'Sector centro de Putre',
        },
    ]
    farmacias = {}
    for item in datos:
        farmacia, _ = Sucursal.objects.get_or_create(
            nombre=item['nombre'],
            defaults={
                'region': item['region'],
                'provincia': item['provincia'],
                'comuna': item['comuna'],
                'direccion': item['direccion'],
                'telefono': '',
                'activo': True,
            },
        )
        farmacia.region = item['region']
        farmacia.provincia = item['provincia']
        farmacia.comuna = item['comuna']
        farmacia.direccion = item['direccion']
        farmacia.activo = True
        farmacia.save()
        farmacias[item['nombre']] = farmacia
    return farmacias


def crear_motos():
    datos = [
        ('CV-AR-101', 'Honda', 'XR 150L', 2022, 'Rojo'),
        ('CV-AR-102', 'Yamaha', 'FZ 150', 2021, 'Verde'),
        ('CV-AR-103', 'Suzuki', 'GN 125', 2020, 'Negro'),
        ('CV-AR-104', 'Honda', 'CB 125F', 2023, 'Blanco'),
        ('CV-AR-105', 'Bajaj', 'Boxer 150', 2022, 'Azul'),
    ]
    motos = {}
    for placa, marca, modelo, anio, color in datos:
        moto, _ = Moto.objects.get_or_create(
            placa=placa,
            defaults={
                'marca': marca,
                'modelo': modelo,
                'año': anio,
                'color': color,
                'estado': 'disponible',
                'activo': True,
            },
        )
        moto.marca = marca
        moto.modelo = modelo
        moto.año = anio
        moto.color = color
        moto.estado = 'disponible'
        moto.activo = True
        moto.save()
        motos[placa] = moto
    return motos


def crear_motoristas(departamentos, farmacias, motos):
    datos = [
        {
            'username': 'motorista_vega',
            'first_name': 'Carlos',
            'last_name': 'Vega',
            'rut': '17555111-1',
            'telefono': '+56961111111',
            'licencia': 'LIC-AR-001',
            'moto': 'CV-AR-101',
            'farmacia': 'Cruz Verde Arica Centro',
            'region': 'Arica',
            'provincia': 'Arica',
            'comuna': 'Arica',
            'direccion': 'Sector centro de Arica',
        },
        {
            'username': 'motorista_rojas',
            'first_name': 'Paula',
            'last_name': 'Rojas',
            'rut': '17666222-2',
            'telefono': '+56962222222',
            'licencia': 'LIC-AR-002',
            'moto': 'CV-AR-102',
            'farmacia': 'Cruz Verde Mall Plaza Arica',
            'region': 'Arica',
            'provincia': 'Arica',
            'comuna': 'Arica',
            'direccion': 'Sector Diego Portales, Arica',
        },
        {
            'username': 'motorista_condori',
            'first_name': 'Luis',
            'last_name': 'Condori',
            'rut': '17777333-3',
            'telefono': '+56963333333',
            'licencia': 'LIC-AR-003',
            'moto': 'CV-AR-103',
            'farmacia': 'Cruz Verde Santa María Arica',
            'region': 'Arica',
            'provincia': 'Arica',
            'comuna': 'Arica',
            'direccion': 'Sector Santa María, Arica',
        },
        {
            'username': 'motorista_mamani',
            'first_name': 'Elena',
            'last_name': 'Mamani',
            'rut': '17888444-4',
            'telefono': '+56964444444',
            'licencia': 'LIC-PA-001',
            'moto': 'CV-AR-104',
            'farmacia': 'Cruz Verde Putre Referencial',
            'region': 'Parinacota',
            'provincia': 'Parinacota',
            'comuna': 'Putre',
            'direccion': 'Sector centro de Putre',
        },
    ]
    for item in datos:
        usuario = crear_usuario(
            username=item['username'],
            password=PASSWORDS[item['username']],
            first_name=item['first_name'],
            last_name=item['last_name'],
            email=f"{item['username']}@cruzverde.local",
            rut=item['rut'],
            telefono=item['telefono'],
            rol='motorista',
            departamento=departamentos['Operación'],
        )
        motorista, _ = Motorista.objects.get_or_create(
            usuario=usuario,
            defaults={
                'licencia': item['licencia'],
                'tipo_licencia': 'C',
                'vigencia_licencia': date(2028, 12, 31),
            },
        )
        motorista.licencia = item['licencia']
        motorista.tipo_licencia = 'C'
        motorista.vigencia_licencia = date(2028, 12, 31)
        motorista.region = item['region']
        motorista.provincia = item['provincia']
        motorista.comuna = item['comuna']
        motorista.direccion = item['direccion']
        motorista.estado = 'disponible'
        motorista.activo = True
        motorista.save()
        sincronizar_asignacion(
            motorista,
            motos[item['moto']],
            farmacias[item['farmacia']],
        )


def crear_despachos_prueba():
    datos = [
        ('COD-1001', 'Av. Providencia 1234, Arica', 'motorista_vega', 'pendiente'),
        ('COD-1002', 'Las Condes 456, Arica', 'motorista_vega', 'en_ruta'),
        ('COD-1003', 'Av. Santa María 900, Arica', 'motorista_rojas', 'pendiente'),
        ('COD-1004', 'Diego Portales 1200, Arica', 'motorista_rojas', 'incidencia'),
        ('COD-1005', 'Baquedano 450, Arica', 'motorista_condori', 'pendiente'),
        ('COD-1006', 'Arturo Prat 300, Putre', 'motorista_mamani', 'pendiente'),
    ]
    for codigo, direccion, username, estado in datos:
        motorista = Motorista.objects.filter(usuario__user__username=username).first()
        if motorista is None:
            continue
        sucursal = motorista.sucursal_actual
        origen = sucursal.direccion_completa if sucursal else ''
        movimiento, _ = Movimiento.objects.get_or_create(
            numero_despacho=codigo,
            defaults={
                'direccion_destino': direccion,
                'direccion_origen': origen,
                'motorista': motorista,
                'sucursal': sucursal,
                'estado': estado,
            },
        )
        movimiento.direccion_destino = direccion
        movimiento.direccion_origen = origen
        movimiento.motorista = motorista
        movimiento.sucursal = sucursal
        movimiento.estado = estado
        if estado == 'incidencia':
            movimiento.tipo_incidencia = 'cliente_ausente'
            movimiento.comentario_incidencia = 'Cliente ausente al momento de la visita.'
        movimiento.save()


def main():
    departamentos = crear_departamentos()
    crear_usuario(
        username='admin_arica',
        password=PASSWORDS['admin_arica'],
        first_name='Admin',
        last_name='Arica',
        email='admin_arica@cruzverde.local',
        rut='11111111-1',
        telefono='+56960000001',
        rol='administrador',
        departamento=departamentos['Administración'],
        is_staff=True,
        is_superuser=True,
    )
    crear_usuario(
        username='despacho_arica',
        password=PASSWORDS['despacho_arica'],
        first_name='Usuario',
        last_name='Despacho',
        email='despacho_arica@cruzverde.local',
        rut='12222222-2',
        telefono='+56960000002',
        rol='supervisor',
        departamento=departamentos['Despacho'],
        is_staff=True,
    )
    crear_usuario(
        username='operador_arica',
        password=PASSWORDS['operador_arica'],
        first_name='Usuario',
        last_name='Operador',
        email='operador_arica@cruzverde.local',
        rut='13333333-3',
        telefono='+56960000003',
        rol='operador',
        departamento=departamentos['Operación'],
    )

    farmacias = crear_farmacias()
    motos = crear_motos()
    crear_motoristas(departamentos, farmacias, motos)
    crear_despachos_prueba()

    print('Datos de prueba cargados correctamente.')
    print('Revise README_DATOS_PRUEBA.md para usuarios y contraseñas.')


if __name__ == '__main__':
    main()
