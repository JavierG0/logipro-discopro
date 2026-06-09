from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from apps.usuarios.models import Usuario, Departamento
from apps.motoristas.models import Motorista
from apps.motoristas.models import Sucursal
from apps.movimientos.models import Movimiento


class UsuarioModelTest(TestCase):
    """Pruebas para el modelo Usuario"""

    def setUp(self):
        self.dept = Departamento.objects.create(
            nombre='Test',
            tipo='operacion',
            descripcion='Departamento de prueba'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Usuario'
        )

    def test_crear_usuario(self):
        """Test crear usuario correctamente"""
        usuario = Usuario.objects.create(
            user=self.user,
            rut='12345678-9',
            departamento=self.dept
        )
        self.assertEqual(usuario.user.username, 'testuser')
        self.assertEqual(usuario.departamento.nombre, 'Test')
        self.assertEqual(usuario.rut, '12345678-9')

    def test_usuario_string(self):
        """Test string representación de usuario"""
        usuario = Usuario.objects.create(
            user=self.user,
            rut='12345678-9',
            departamento=self.dept
        )
        self.assertEqual(str(usuario), 'Test Usuario (12345678-9)')


class MotoristaModelTest(TestCase):
    """Pruebas para el modelo Motorista"""

    def setUp(self):
        self.dept = Departamento.objects.create(
            nombre='Motorista',
            tipo='operacion',
            descripcion='Departamento motorista'
        )
        self.user = User.objects.create_user(
            username='motorista1',
            email='motorista@test.com',
            password='testpass123',
            first_name='Juan',
            last_name='Pérez'
        )
        self.usuario = Usuario.objects.create(
            user=self.user,
            rut='98765432-1',
            departamento=self.dept
        )

    def test_crear_motorista(self):
        """Test crear motorista"""
        motorista = Motorista.objects.create(
            usuario=self.usuario,
            licencia='LIC001',
            tipo_licencia='B',
            vigencia_licencia='2026-12-31',
            vehiculo_placa='NQB-123',
            estado='disponible'
        )
        self.assertEqual(motorista.licencia, 'LIC001')
        self.assertEqual(motorista.estado, 'disponible')

    def test_licencia_unica(self):
        """Test que la licencia sea única"""
        Motorista.objects.create(
            usuario=self.usuario,
            licencia='LIC001',
            tipo_licencia='B',
            vigencia_licencia='2026-12-31',
            vehiculo_placa='NQB-123'
        )

        user2 = User.objects.create_user(
            username='motorista2',
            email='motorista2@test.com',
            password='testpass123',
            first_name='Ana',
            last_name='Gómez'
        )
        usuario2 = Usuario.objects.create(
            user=user2,
            rut='87654321-0',
            departamento=self.dept
        )

        with self.assertRaises(Exception):
            Motorista.objects.create(
                usuario=usuario2,
                licencia='LIC001',  # Licencia duplicada
                tipo_licencia='B',
                vigencia_licencia='2026-12-31',
                vehiculo_placa='NQB-456'
            )


class LoginTest(TestCase):
    """Pruebas para el login"""

    def setUp(self):
        self.client = Client()
        self.dept = Departamento.objects.create(
            nombre='Admin',
            tipo='admin',
            descripcion='Departamento administrador'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Usuario'
        )
        Usuario.objects.create(
            user=self.user,
            rut='11111111-1',
            departamento=self.dept
        )

    def test_login_page_accesible(self):
        """Test que la página de login sea accesible"""
        response = self.client.get(reverse('usuarios:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_correcto(self):
        """Test login con credenciales correctas"""
        response = self.client.post(reverse('usuarios:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        }, follow=True)
        self.assertTrue(response.wsgi_request.user.is_authenticated)


class MovimientoModelTest(TestCase):
    """Pruebas para el modelo Movimiento"""

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test',
            direccion='Calle Test 123',
            ciudad='Bogotá',
            telefono='3101234567',
            email='test@sucursal.com',
            latitud=0.0,
            longitud=0.0
        )

        self.dept = Departamento.objects.create(
            nombre='Motorista',
            tipo='operacion',
            descripcion='Departamento motorista'
        )
        self.user = User.objects.create_user(
            username='motorista1',
            email='motorista@test.com',
            password='testpass123',
            first_name='Juan',
            last_name='Pérez'
        )
        self.usuario = Usuario.objects.create(
            user=self.user,
            rut='98765432-1',
            departamento=self.dept
        )
        self.motorista = Motorista.objects.create(
            usuario=self.usuario,
            licencia='LIC001',
            tipo_licencia='B',
            vigencia_licencia='2026-12-31',
            vehiculo_placa='NQB-123'
        )

    def test_crear_movimiento(self):
        """Test crear movimiento"""
        movimiento = Movimiento.objects.create(
            numero_despacho='DSP001',
            motorista=self.motorista,
            sucursal=self.sucursal,
            tipo_movimiento='entrega',
            descripcion='Entrega de medicamentos',
            fecha_programada=timezone.now()
        )
        self.assertEqual(movimiento.numero_despacho, 'DSP001')
        self.assertEqual(movimiento.estado, 'pendiente')

    def test_despacho_numero_unico(self):
        """Test que el número de despacho sea único"""
        Movimiento.objects.create(
            numero_despacho='DSP001',
            motorista=self.motorista,
            sucursal=self.sucursal,
            tipo_movimiento='entrega',
            descripcion='Entrega de medicamentos',
            fecha_programada=timezone.now()
        )

        with self.assertRaises(Exception):
            Movimiento.objects.create(
                numero_despacho='DSP001',  # Número duplicado
                motorista=self.motorista,
                sucursal=self.sucursal,
                tipo_movimiento='retiro',
                descripcion='Retiro de receta',
                fecha_programada=timezone.now()
            )


class SucursalModelTest(TestCase):
    """Pruebas para el modelo Sucursal"""

    def test_crear_sucursal(self):
        """Test crear sucursal"""
        sucursal = Sucursal.objects.create(
            nombre='Sucursal Centro',
            direccion='Calle Principal 123',
            ciudad='Bogotá',
            telefono='3101234567',
            email='centro@sucursal.com',
            latitud=0.0,
            longitud=0.0
        )
        self.assertEqual(sucursal.nombre, 'Sucursal Centro')
        self.assertEqual(sucursal.ciudad, 'Bogotá')

    def test_email_guardado(self):
        """Test que el email de sucursal se guarda correctamente"""
        sucursal = Sucursal.objects.create(
            nombre='Sucursal 1',
            direccion='Calle 1',
            ciudad='Bogotá',
            telefono='3101234567',
            email='info@sucursal.com',
            latitud=0.0,
            longitud=0.0
        )
        self.assertEqual(sucursal.email, 'info@sucursal.com')
