"""
Suite de pruebas unitarias e integración — LogiPro / Discopro Django.
Alineada al sistema actual (modelos, vistas y reglas de negocio vigentes).
"""
from datetime import date

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from apps.motoristas.geografia import comunas, provincias, regiones
from apps.motoristas.models import AsignacionOperativa, Moto, Motorista, Sucursal, sincronizar_asignacion
from apps.movimientos.models import Movimiento
from apps.movimientos.utils import filtrar_movimientos, motorista_pertenece_a_farmacia, validar_asignacion_movimiento
from apps.usuarios.models import Departamento, Usuario
from apps.usuarios.permissions import es_administrador_sistema, puede_gestionar_flota


class BaseLogiProTestCase(TestCase):
    """Fixtures compartidas para el dominio logístico actual."""

    @classmethod
    def crear_usuario_sistema(cls, username, rut, rol='operador', password='testpass123'):
        dept = Departamento.objects.create(
            nombre=f'Dept {username}',
            tipo='operacion',
            descripcion='Prueba',
        )
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name='Nombre',
            last_name='Apellido',
        )
        perfil = Usuario.objects.create(
            user=user,
            rut=rut,
            rol=rol,
            departamento=dept,
        )
        return user, perfil

    @classmethod
    def crear_farmacia(cls, nombre, region='Arica', provincia='Arica', comuna='Arica', direccion='Calle 1'):
        return Sucursal.objects.create(
            nombre=nombre,
            region=region,
            provincia=provincia,
            comuna=comuna,
            direccion=direccion,
            activo=True,
        )

    @classmethod
    def crear_motorista_operativo(cls, username, rut, licencia, farmacia, moto=None):
        user, perfil = cls.crear_usuario_sistema(username, rut, rol='motorista')
        motorista = Motorista.objects.create(
            usuario=perfil,
            licencia=licencia,
            tipo_licencia='C',
            vigencia_licencia=date(2028, 12, 31),
            region=farmacia.region,
            provincia=farmacia.provincia,
            comuna=farmacia.comuna,
            estado='disponible',
            activo=True,
        )
        sincronizar_asignacion(motorista, moto, farmacia)
        return motorista


# ─── Autenticación ───────────────────────────────────────────────────────────

class AutenticacionTest(BaseLogiProTestCase):
    def setUp(self):
        self.client = Client()
        self.user, _ = self.crear_usuario_sistema('operador_test', '11111111-1', rol='operador')

    def test_login_page_accesible(self):
        response = self.client.get(reverse('usuarios:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'LogiPro')

    def test_login_correcto_operador(self):
        response = self.client.post(reverse('usuarios:login'), {
            'username': 'operador_test',
            'password': 'testpass123',
        }, follow=True)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('home'))

    def test_login_incorrecto_rechazado(self):
        response = self.client.post(reverse('usuarios:login'), {
            'username': 'operador_test',
            'password': 'malpassword',
        })
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_redireccion_motorista_al_portal(self):
        self.crear_motorista_operativo(
            'motorista_test', '22222222-2', 'LIC-T01',
            self.crear_farmacia('Farmacia Portal'),
        )
        response = self.client.post(reverse('usuarios:login'), {
            'username': 'motorista_test',
            'password': 'testpass123',
        }, follow=True)
        self.assertRedirects(response, reverse('portal_motorista:inicio'))


# ─── Usuarios y roles ────────────────────────────────────────────────────────

class UsuarioModelTest(BaseLogiProTestCase):
    def test_crear_usuario_perfil(self):
        user, perfil = self.crear_usuario_sistema('admin_test', '33333333-3', rol='administrador')
        self.assertEqual(perfil.user.username, 'admin_test')
        self.assertEqual(perfil.rut, '33333333-3')
        self.assertEqual(perfil.rol, 'administrador')

    def test_usuario_string_muestra_rol(self):
        _, perfil = self.crear_usuario_sistema('op1', '44444444-4', rol='operador')
        self.assertEqual(str(perfil), 'Nombre Apellido (Operadora)')

    def test_permisos_por_rol(self):
        admin_user, _ = self.crear_usuario_sistema('adm', '55555555-5', rol='administrador')
        sup_user, _ = self.crear_usuario_sistema('sup', '66666666-6', rol='supervisor')
        op_user, _ = self.crear_usuario_sistema('op', '77777777-7', rol='operador')
        self.assertTrue(es_administrador_sistema(admin_user))
        self.assertTrue(puede_gestionar_flota(sup_user))
        self.assertFalse(puede_gestionar_flota(op_user))


# ─── Farmacias origen ───────────────────────────────────────────────────────

class FarmaciaModelTest(BaseLogiProTestCase):
    def test_crear_farmacia_con_geografia(self):
        farmacia = self.crear_farmacia('CV Arica Centro')
        self.assertEqual(farmacia.region, 'Arica')
        self.assertIn('Arica', farmacia.direccion_completa)

    def test_regiones_arica_y_parinacota_separadas(self):
        self.assertIn('Arica', regiones())
        self.assertIn('Parinacota', regiones())
        self.assertNotIn('Arica y Parinacota', regiones())

    def test_cascada_geografica_putre(self):
        prov = provincias('Parinacota')
        self.assertIn('Parinacota', prov)
        self.assertIn('Putre', comunas('Parinacota', 'Parinacota'))


# ─── Motoristas y asignaciones ───────────────────────────────────────────────

class MotoristaAsignacionTest(BaseLogiProTestCase):
    def setUp(self):
        self.farmacia_a = self.crear_farmacia('Farmacia Arica')
        self.farmacia_b = self.crear_farmacia('Farmacia Putre', region='Parinacota', provincia='Parinacota', comuna='Putre')
        self.moto = Moto.objects.create(placa='TST-001', marca='Honda', modelo='XR', año=2022, activo=True)
        self.motorista = self.crear_motorista_operativo('mot_a', '88888888-8', 'LIC-A01', self.farmacia_a, self.moto)

    def test_crear_motorista_con_asignacion(self):
        self.assertEqual(self.motorista.sucursal_actual, self.farmacia_a)
        self.assertEqual(self.motorista.moto_actual, self.moto)

    def test_licencia_unica(self):
        user2, perfil2 = self.crear_usuario_sistema('mot_b', '99999999-9', rol='motorista')
        with self.assertRaises(IntegrityError):
            Motorista.objects.create(
                usuario=perfil2,
                licencia='LIC-A01',
                tipo_licencia='C',
                vigencia_licencia=date(2028, 12, 31),
            )

    def test_sincronizar_asignacion_desactiva_anterior(self):
        sincronizar_asignacion(self.motorista, self.moto, self.farmacia_b)
        activas = AsignacionOperativa.objects.filter(motorista=self.motorista, activa=True)
        self.assertEqual(activas.count(), 1)
        self.assertEqual(self.motorista.sucursal_actual, self.farmacia_b)


# ─── Movimientos ─────────────────────────────────────────────────────────────

class MovimientoModelTest(BaseLogiProTestCase):
    def setUp(self):
        self.farmacia = self.crear_farmacia('Origen Test', direccion='Av. 21 de Mayo 100')
        self.motorista = self.crear_motorista_operativo('mot_mov', '10101010-1', 'LIC-M01', self.farmacia)

    def test_crear_movimiento_estado_pendiente(self):
        mov = Movimiento.objects.create(
            numero_despacho='DESP-9001',
            sucursal=self.farmacia,
            direccion_destino='Destino 456',
            motorista=self.motorista,
        )
        self.assertEqual(mov.estado, 'pendiente')

    def test_direccion_origen_autocompletada(self):
        mov = Movimiento.objects.create(
            numero_despacho='DESP-9002',
            sucursal=self.farmacia,
            direccion_destino='Destino 789',
            motorista=self.motorista,
        )
        self.assertTrue(mov.direccion_origen)
        self.assertIn('21 de Mayo', mov.direccion_origen)

    def test_numero_despacho_unico_global(self):
        Movimiento.objects.create(
            numero_despacho='DESP-UNICO',
            sucursal=self.farmacia,
            direccion_destino='Destino',
            motorista=self.motorista,
        )
        with self.assertRaises(IntegrityError):
            Movimiento.objects.create(
                numero_despacho='DESP-UNICO',
                sucursal=self.farmacia,
                direccion_destino='Otro destino',
                motorista=self.motorista,
            )


class ValidacionAsignacionTest(BaseLogiProTestCase):
    def setUp(self):
        self.farmacia_arica = self.crear_farmacia('CV Arica')
        self.farmacia_putre = self.crear_farmacia(
            'CV Putre', region='Parinacota', provincia='Parinacota', comuna='Putre',
        )
        self.motorista_arica = self.crear_motorista_operativo(
            'mot_arica', '12121212-1', 'LIC-R01', self.farmacia_arica,
        )

    def test_motorista_pertenece_a_su_farmacia(self):
        self.assertTrue(motorista_pertenece_a_farmacia(self.motorista_arica, self.farmacia_arica))

    def test_motorista_no_pertenece_a_otra_farmacia(self):
        self.assertFalse(motorista_pertenece_a_farmacia(self.motorista_arica, self.farmacia_putre))

    def test_validar_asignacion_retorna_error_cruzado(self):
        error = validar_asignacion_movimiento(self.motorista_arica, self.farmacia_putre)
        self.assertIsNotNone(error)
        self.assertIn('CV Arica', error)
        self.assertIn('CV Putre', error)

    def test_validar_asignacion_ok_misma_farmacia(self):
        self.assertIsNone(validar_asignacion_movimiento(self.motorista_arica, self.farmacia_arica))


# ─── Integración dashboard ───────────────────────────────────────────────────

class DashboardIntegracionTest(BaseLogiProTestCase):
    def setUp(self):
        self.client = Client()
        self.operador, _ = self.crear_usuario_sistema('operador_dash', '13131313-1', rol='operador')
        self.farmacia = self.crear_farmacia('Farmacia Dash')
        self.otra_farmacia = self.crear_farmacia(
            'Farmacia Lejana', region='Parinacota', provincia='Parinacota', comuna='Putre',
        )
        self.motorista_ok = self.crear_motorista_operativo(
            'mot_dash', '14141414-1', 'LIC-D01', self.farmacia,
        )
        self.motorista_otra = self.crear_motorista_operativo(
            'mot_lejos', '15151515-1', 'LIC-D02', self.otra_farmacia,
        )
        self.client.login(username='operador_dash', password='testpass123')

    def test_registrar_despacho_valido(self):
        response = self.client.post(reverse('home'), {
            'numero_despacho': 'REG-001',
            'sucursal_origen': self.farmacia.pk,
            'motorista': self.motorista_ok.pk,
            'direccion_destino': 'Destino válido 123',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Movimiento.objects.filter(numero_despacho='REG-001').exists())
        mov = Movimiento.objects.get(numero_despacho='REG-001')
        self.assertEqual(mov.sucursal_id, self.farmacia.pk)
        self.assertTrue(mov.direccion_origen)

    def test_rechaza_motorista_de_otra_farmacia(self):
        before = Movimiento.objects.count()
        self.client.post(reverse('home'), {
            'numero_despacho': 'REG-002',
            'sucursal_origen': self.farmacia.pk,
            'motorista': self.motorista_otra.pk,
            'direccion_destino': 'Destino inválido',
        })
        self.assertEqual(Movimiento.objects.count(), before)

    def test_filtro_movimientos_por_direccion(self):
        Movimiento.objects.create(
            numero_despacho='FIL-001',
            sucursal=self.farmacia,
            direccion_origen='Origen centro',
            direccion_destino='Destino providencia',
            motorista=self.motorista_ok,
        )
        qs = filtrar_movimientos(Movimiento.objects.all(), {'q_direccion': 'providencia'})
        self.assertEqual(qs.count(), 1)


# ─── API farmacia ────────────────────────────────────────────────────────────

class ApiFarmaciaTest(BaseLogiProTestCase):
    def setUp(self):
        self.client = Client()
        user, _ = self.crear_usuario_sistema('api_user', '16161616-1', rol='operador')
        self.client.login(username='api_user', password='testpass123')
        self.farmacia = self.crear_farmacia('API Farmacia', direccion='Calle API 50')
        self.motorista = self.crear_motorista_operativo(
            'mot_api', '17171717-1', 'LIC-API', self.farmacia,
        )

    def test_api_direccion_farmacia(self):
        url = reverse('farmacia:api_direccion', kwargs={'pk': self.farmacia.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('Calle API 50', data['direccion'])

    def test_api_motoristas_por_farmacia(self):
        url = reverse('farmacia:api_motoristas', kwargs={'pk': self.farmacia.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        ids = [m['id'] for m in response.json()['motoristas']]
        self.assertIn(self.motorista.pk, ids)


# ─── Portal motorista ────────────────────────────────────────────────────────

class PortalMotoristaTest(BaseLogiProTestCase):
    def setUp(self):
        self.client = Client()
        self.farmacia = self.crear_farmacia('Portal Farmacia')
        self.motorista = self.crear_motorista_operativo(
            'mot_portal', '18181818-1', 'LIC-P01', self.farmacia,
        )
        self.despacho = Movimiento.objects.create(
            numero_despacho='PORT-001',
            sucursal=self.farmacia,
            direccion_destino='Entrega portal',
            motorista=self.motorista,
            estado='pendiente',
        )
        self.client.login(username='mot_portal', password='testpass123')

    def test_iniciar_ruta_cambia_estado(self):
        url = reverse('portal_motorista:iniciar_ruta', kwargs={'pk': self.despacho.pk})
        self.client.get(url)
        self.despacho.refresh_from_db()
        self.assertEqual(self.despacho.estado, 'en_ruta')

    def test_marcar_entregado(self):
        self.despacho.estado = 'en_ruta'
        self.despacho.save()
        url = reverse('portal_motorista:entregado', kwargs={'pk': self.despacho.pk})
        self.client.get(url)
        self.despacho.refresh_from_db()
        self.assertEqual(self.despacho.estado, 'entregado')
        self.assertIsNotNone(self.despacho.entregado_en)

    def test_operador_no_accede_portal(self):
        self.client.logout()
        user, _ = self.crear_usuario_sistema('op_portal', '19191919-1', rol='operador')
        self.client.login(username='op_portal', password='testpass123')
        response = self.client.get(reverse('portal_motorista:inicio'))
        self.assertRedirects(response, reverse('home'))


# ─── Permisos administración ─────────────────────────────────────────────────

class PermisosAccesoTest(BaseLogiProTestCase):
    def setUp(self):
        self.client = Client()

    def test_operador_no_accede_lista_farmacias(self):
        self.crear_usuario_sistema('op_perm', '20202020-1', rol='operador')
        self.client.login(username='op_perm', password='testpass123')
        response = self.client.get(reverse('farmacia:lista'))
        self.assertRedirects(response, reverse('home'))

    def test_supervisor_accede_lista_farmacias(self):
        self.crear_usuario_sistema('sup_perm', '21212121-1', rol='supervisor')
        self.client.login(username='sup_perm', password='testpass123')
        response = self.client.get(reverse('farmacia:lista'))
        self.assertEqual(response.status_code, 200)

    def test_operador_no_accede_admin_usuarios(self):
        self.crear_usuario_sistema('op_admin', '22222222-3', rol='operador')
        self.client.login(username='op_admin', password='testpass123')
        response = self.client.get(reverse('usuarios:lista_sistema'))
        self.assertRedirects(response, reverse('home'))

    def test_administrador_accede_admin_usuarios(self):
        self.crear_usuario_sistema('adm_perm', '23232323-2', rol='administrador')
        self.client.login(username='adm_perm', password='testpass123')
        response = self.client.get(reverse('usuarios:lista_sistema'))
        self.assertEqual(response.status_code, 200)
