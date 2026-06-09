# Discopro - Sistema de Gestión de Distribución con Django

Aplicación web para la gestión de motoristas, movimientos (entregas/retiros) y reportes en tiempo real.

## Características Principales

- **Autenticación y Control de Acceso**: Sistema de login con roles de usuario (Admin, Operador, Motorista, Supervisor)
- **Gestión de Motoristas**: CRUD completo para motoristas con seguimiento de estado
- **Tracking de Movimientos**: Registro de entregas y retiros con seguimiento en tiempo real
- **Reportes**: Generación de reportes por período, motorista o tipo de movimiento
- **API REST**: Endpoints para integración con aplicaciones externas
- **Interfaz Responsiva**: Diseño adaptable a dispositivos móviles

## Requisitos Previos

- Python 3.8+
- MariaDB 10.5+ o MySQL 5.7+
- pip (gestor de paquetes de Python)
- virtualenv (recomendado)

## Instalación

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd Discopro_Django
```

### 2. Crear Entorno Virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

#### Opción A: Usando .env (Recomendado)

1. Asegúrate que MariaDB esté corriendo en tu máquina
2. Crea una base de datos nueva:
   ```sql
   CREATE DATABASE discopro_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Actualiza el archivo `.env` con tus credenciales:
   ```
   DB_NAME=discopro_db
   DB_USER=root
   DB_PASSWORD=tu_contraseña
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```

#### Opción B: Usando HeidiSQL (GUI)

1. Abre HeidiSQL
2. Crea nueva conexión a tu servidor MariaDB
3. Crea nueva base de datos: `discopro_db`
4. Actualiza `.env` con los datos de conexión

### 5. Aplicar Migraciones

```bash
# Crear archivos de migración
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate
```

### 6. Crear Superusuario (Admin)

```bash
python manage.py createsuperuser
```

Ingresa:
- Username: admin
- Email: admin@discopro.com
- Password: tu_contraseña

### 7. Ejecutar el Servidor

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://localhost:8000`

## Acceso Inicial

- **URL**: http://localhost:8000
- **Usuario Admin**: http://localhost:8000/admin
- **Credenciales**: Las que ingresaste en el paso 6

## Estructura del Proyecto

```
Discopro_Django/
├── discopro/                 # Configuración del proyecto
│   ├── settings.py          # Configuración de Django
│   ├── urls.py              # URLs principales
│   ├── wsgi.py              # WSGI para producción
│   └── asgi.py              # ASGI para WebSockets
├── apps/                    # Aplicaciones Django
│   ├── usuarios/            # Gestión de usuarios y autenticación
│   ├── motoristas/          # Gestión de motoristas
│   ├── movimientos/         # Gestión de movimientos
│   ├── reportes/            # Generación de reportes
│   └── api/                 # API REST
├── templates/               # Plantillas HTML
├── static/                  # Archivos estáticos (CSS, JS)
│   ├── css/
│   └── js/
├── media/                   # Archivos subidos por usuarios
├── requirements.txt         # Dependencias del proyecto
├── .env                     # Variables de entorno (no incluir en git)
└── manage.py               # Herramienta de administración de Django
```

## Rutas Principales

### Autenticación
- `GET /login/` - Formulario de login
- `POST /login/` - Procesar login
- `GET /logout/` - Cerrar sesión
- `GET /registro/` - Formulario de registro
- `POST /registro/` - Crear nuevo usuario

### Aplicación
- `GET /dashboard/` - Panel principal
- `GET /motoristas/` - Lista de motoristas
- `GET /motoristas/<id>/` - Detalle de motorista
- `GET /movimientos/` - Lista de movimientos
- `GET /movimientos/<id>/` - Detalle de movimiento
- `GET /reportes/` - Reportes

### API REST
- `GET /api/motoristas/` - Lista de motoristas (JSON)
- `POST /api/motoristas/` - Crear motorista
- `GET /api/movimientos/` - Lista de movimientos
- `POST /api/movimientos/` - Crear movimiento
- `GET /api/reportes/` - Lista de reportes

## Tecnologías Utilizadas

- **Backend**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Base de Datos**: MariaDB / MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6

## Configuración de Producción

Para desplegar en producción:

1. Actualiza `DEBUG = False` en `settings.py`
2. Cambia `SECRET_KEY` a un valor seguro y aleatorio
3. Configura `ALLOWED_HOSTS` con tu dominio
4. Usa Gunicorn como servidor WSGI:
   ```bash
   pip install gunicorn
   gunicorn discopro.wsgi:application
   ```
5. Configura un servidor web (Nginx/Apache) como reverse proxy
6. Usa SSL/TLS para HTTPS

## Comandos Útiles

```bash
# Crear superusuario
python manage.py createsuperuser

# Hacer migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear migraciones para una app específica
python manage.py makemigrations usuarios

# Ver estado de migraciones
python manage.py showmigrations

# Deshacer últimas migraciones
python manage.py migrate usuarios zero

# Vaciar datos (cuidado)
python manage.py flush

# Recopilar archivos estáticos
python manage.py collectstatic

# Crear datos de prueba
python manage.py shell < seed.py

# Ejecutar pruebas
python manage.py test

# Análisis del código
python manage.py check
```

## Permisos y Roles

### Admin
- Acceso completo a todas las funciones
- Gestión de usuarios
- Ver todos los reportes

### Operador
- Crear y editar movimientos
- Ver motoristas
- Generar reportes

### Motorista
- Ver sus propios movimientos
- Actualizar estado de movimientos asignados
- Ver ubicación

### Supervisor
- Ver todos los movimientos
- Generar reportes
- Ver analíticas

## Solución de Problemas

### Error: "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Error: "Can't connect to MySQL server"
- Verifica que MariaDB esté corriendo
- Revisa credenciales en `.env`
- Verifica host y puerto

### Error de migraciones
```bash
python manage.py migrate --fake-initial
```

### Archivos estáticos no cargando
```bash
python manage.py collectstatic
```

## Soporte y Documentación

- [Documentación de Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [MariaDB Documentation](https://mariadb.com/docs/)

## Licencia

Este proyecto está bajo licencia MIT.

## Autor

Discopro Development Team

---

**Última actualización**: 2024
**Versión**: 1.0.0
