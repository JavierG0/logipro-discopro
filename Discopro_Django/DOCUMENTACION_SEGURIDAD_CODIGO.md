# Documentacion de seguridad aplicada en el codigo fuente

Proyecto: **Discopro Django - Cruz Verde**

Este documento identifica los patrones de seguridad aplicados en el codigo fuente, indicando **archivo**, **lineas exactas**, **fragmento de codigo** y **descripcion de seguridad**.

---

## 1. Configuracion de secretos por variables de entorno

**Archivo:** `Discopro_Django/discopro/settings.py`  
**Lineas:** 14-16

```14:16:Discopro_Django/discopro/settings.py
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-change-in-production')

DEBUG = config('DEBUG', default=True, cast=bool)
```

**Descripcion de seguridad:**  
El proyecto usa `python-decouple` para leer configuraciones sensibles desde variables de entorno. Esto permite separar secretos como `SECRET_KEY` y `DEBUG` del codigo fuente. En produccion, `SECRET_KEY` debe venir desde el archivo `.env` o desde variables del servidor, evitando exponer claves reales dentro del repositorio.

---

## 2. Middleware de seguridad HTTP

**Archivo:** `Discopro_Django/discopro/settings.py`  
**Lineas:** 36-45

```36:45:Discopro_Django/discopro/settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Descripcion de seguridad:**  
Esta cadena protege todas las peticiones antes de llegar a las vistas:

- `SecurityMiddleware`: agrega protecciones HTTP generales.
- `SessionMiddleware`: habilita sesiones seguras para usuarios autenticados.
- `CsrfViewMiddleware`: valida tokens CSRF en formularios POST.
- `AuthenticationMiddleware`: agrega `request.user` para controlar autenticacion.
- `XFrameOptionsMiddleware`: reduce riesgos de clickjacking evitando que la app sea cargada en iframes no autorizados.

---

## 3. Proteccion CSRF en formularios

**Archivo:** `Discopro_Django/templates/login.html`  
**Lineas:** 124-125

```124:125:Discopro_Django/templates/login.html
        <form method="POST" action="{% url 'usuarios:login' %}">
            {% csrf_token %}
```

**Archivo:** `Discopro_Django/discopro/settings.py`  
**Linea:** 41

```41:41:Discopro_Django/discopro/settings.py
    'django.middleware.csrf.CsrfViewMiddleware',
```

**Descripcion de seguridad:**  
El token CSRF evita que un sitio externo envie formularios en nombre de un usuario autenticado. El template incluye `{% csrf_token %}` y el middleware verifica que el token recibido sea valido antes de permitir el POST. Este patron se aplica tambien en formularios como dashboard, CRUD de farmacias, motos, motoristas, reportes e incidencias.

---

## 4. Autenticacion de usuarios con Django Auth

**Archivo:** `Discopro_Django/apps/usuarios/views.py`  
**Lineas:** 18-43

```18:43:Discopro_Django/apps/usuarios/views.py
@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vista de login de usuarios"""
    # Si el usuario ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect(redireccion_por_rol(request.user))
        
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
            return redirect(redireccion_por_rol(user))
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'login.html')
```

**Descripcion de seguridad:**  
La autenticacion se realiza con `authenticate()`, funcion oficial de Django para validar usuario y contrasena usando el sistema de hashing interno. Si las credenciales son correctas, `login()` crea la sesion del usuario. Esto evita manejar manualmente contrasenas o sesiones.

Ademas, `@require_http_methods(["GET", "POST"])` limita la vista de login solo a los metodos necesarios.

---

## 5. Redireccion por rol despues del login

**Archivo:** `Discopro_Django/apps/usuarios/views.py`  
**Lineas:** 10-16

```10:16:Discopro_Django/apps/usuarios/views.py
def redireccion_por_rol(user):
    try:
        if user.usuario_profile.rol == 'motorista':
            return 'portal_motorista:inicio'
    except Usuario.DoesNotExist:
        pass
    return 'home'
```

**Descripcion de seguridad:**  
Despues del login, los motoristas son enviados al portal exclusivo de motoristas y los demas usuarios al panel principal. Esto ayuda a separar los flujos de trabajo y reduce la posibilidad de que un motorista acceda por error a pantallas administrativas.

---

## 6. Cierre de sesion protegido

**Archivo:** `Discopro_Django/apps/usuarios/views.py`  
**Lineas:** 46-51

```46:51:Discopro_Django/apps/usuarios/views.py
@login_required(login_url='usuarios:login')
def logout_view(request):
    """Vista de cierre de sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('usuarios:login')
```

**Descripcion de seguridad:**  
La funcion `logout()` elimina la sesion activa del usuario. El decorador `@login_required` asegura que solo usuarios autenticados puedan ejecutar el cierre de sesion.

---

## 7. Proteccion de vistas con `@login_required`

**Archivo:** `Discopro_Django/apps/motoristas/portal_views.py`  
**Lineas:** 27-29

```27:29:Discopro_Django/apps/motoristas/portal_views.py
@login_required(login_url='usuarios:login')
@motorista_requerido
def inicio(request):
```

**Descripcion de seguridad:**  
`@login_required` impide el acceso a usuarios anonimos. Si alguien intenta abrir una ruta protegida sin iniciar sesion, Django lo redirige al login. Este patron se usa en el portal motorista, perfil de usuario, movimientos, reportes y dashboard.

---

## 8. Control de acceso por roles (RBAC)

**Archivo:** `Discopro_Django/apps/usuarios/permissions.py`  
**Lineas:** 9-17

```9:17:Discopro_Django/apps/usuarios/permissions.py
def obtener_rol(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser:
        return 'administrador'
    try:
        return user.usuario_profile.rol
    except Usuario.DoesNotExist:
        return None
```

**Descripcion de seguridad:**  
La funcion `obtener_rol()` centraliza la lectura del rol del usuario. Si el usuario no esta autenticado, devuelve `None`; si es superusuario, lo trata como administrador. Esto permite aplicar reglas de permisos segun el perfil.

---

## 9. Permiso para gestion de flota

**Archivo:** `Discopro_Django/apps/usuarios/permissions.py`  
**Lineas:** 24-27

```24:27:Discopro_Django/apps/usuarios/permissions.py
def puede_gestionar_flota(user):
    """Admin y despachador pueden gestionar farmacias, motos y motoristas."""
    rol = obtener_rol(user)
    return user.is_superuser or rol in ('administrador', 'despachador')
```

**Descripcion de seguridad:**  
Solo los usuarios con rol `administrador`, `despachador` o superusuario pueden gestionar farmacias, motos y motoristas. El rol `operador` queda fuera de esta funcion, por lo que no deberia acceder a pantallas de administracion de flota.

---

## 10. Decorador de autorizacion administrativa

**Archivo:** `Discopro_Django/apps/usuarios/permissions.py`  
**Lineas:** 30-37

```30:37:Discopro_Django/apps/usuarios/permissions.py
def administrador_requerido(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not puede_gestionar_flota(request.user):
            messages.error(request, 'No tiene permisos para acceder a esta sección.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
```

**Descripcion de seguridad:**  
Este decorador bloquea vistas administrativas si el usuario no tiene permiso de gestion de flota. En caso de no cumplir, se muestra un mensaje de error y se redirige al inicio. Es un ejemplo de autorizacion en servidor, no solo ocultamiento visual.

---

## 11. Decorador exclusivo para motoristas

**Archivo:** `Discopro_Django/apps/motoristas/portal_views.py`  
**Lineas:** 11-17

```11:17:Discopro_Django/apps/motoristas/portal_views.py
def motorista_requerido(view_func):
    def wrapper(request, *args, **kwargs):
        if obtener_rol(request.user) != 'motorista':
            messages.error(request, 'Este portal es exclusivo para motoristas.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
```

**Descripcion de seguridad:**  
Este decorador impide que administradores, operadores o despachadores entren al portal exclusivo de motoristas. Tambien evita que usuarios autenticados con otro rol manipulen rutas del portal.

---

## 12. Obtencion segura del motorista actual

**Archivo:** `Discopro_Django/apps/motoristas/portal_views.py`  
**Lineas:** 20-24

```20:24:Discopro_Django/apps/motoristas/portal_views.py
def _motorista_actual(request):
    return get_object_or_404(
        Motorista.objects.select_related('usuario__user', 'moto', 'sucursal'),
        usuario__user=request.user,
    )
```

**Descripcion de seguridad:**  
El sistema obtiene el motorista usando el usuario autenticado (`request.user`). Esto evita que el usuario envie manualmente un ID de motorista por URL o formulario para suplantar a otro motorista.

---

## 13. Aislamiento de datos del motorista (anti-IDOR)

**Archivo:** `Discopro_Django/apps/motoristas/portal_views.py`  
**Lineas:** 50-55

```50:55:Discopro_Django/apps/motoristas/portal_views.py
@login_required(login_url='usuarios:login')
@motorista_requerido
def detalle_despacho(request, pk):
    motorista = _motorista_actual(request)
    despacho = get_object_or_404(Movimiento.objects.select_related('sucursal'), pk=pk, motorista=motorista)
    return render(request, 'motorista_portal/detalle_despacho.html', {'motorista': motorista, 'despacho': despacho})
```

**Descripcion de seguridad:**  
Esta consulta filtra por `pk` y por `motorista=motorista`. Aunque un motorista adivine el ID de un despacho ajeno, la consulta no lo devuelve. Si el despacho no pertenece al motorista autenticado, Django responde con 404. Esto previene IDOR (Insecure Direct Object Reference).

---

## 14. Proteccion de acciones del despacho

**Archivo:** `Discopro_Django/apps/motoristas/portal_views.py`  
**Lineas:** 58-67

```58:67:Discopro_Django/apps/motoristas/portal_views.py
@login_required(login_url='usuarios:login')
@motorista_requerido
def iniciar_ruta(request, pk):
    motorista = _motorista_actual(request)
    despacho = get_object_or_404(Movimiento, pk=pk, motorista=motorista)
    if despacho.estado == 'pendiente':
        despacho.estado = 'en_ruta'
        despacho.save(update_fields=['estado', 'actualizado_en'])
        messages.success(request, 'Ruta iniciada.')
    return redirect('portal_motorista:detalle', pk=despacho.pk)
```

**Descripcion de seguridad:**  
La accion de iniciar ruta solo puede ejecutarse si el usuario esta autenticado, tiene rol motorista y el despacho pertenece a ese motorista. Ademas, solo cambia el estado si el despacho esta `pendiente`, evitando transiciones no validas.

---

## 15. Marcado de entrega con control de propiedad

**Archivo:** `Discopro_Django/apps/motoristas/portal_views.py`  
**Lineas:** 70-80

```70:80:Discopro_Django/apps/motoristas/portal_views.py
@login_required(login_url='usuarios:login')
@motorista_requerido
def marcar_entregado(request, pk):
    motorista = _motorista_actual(request)
    despacho = get_object_or_404(Movimiento, pk=pk, motorista=motorista)
    if despacho.estado in ('pendiente', 'en_ruta'):
        despacho.estado = 'entregado'
        despacho.entregado_en = timezone.now()
        despacho.save(update_fields=['estado', 'entregado_en', 'actualizado_en'])
        messages.success(request, 'Despacho marcado como entregado.')
    return redirect('portal_motorista:detalle', pk=despacho.pk)
```

**Descripcion de seguridad:**  
El motorista solo puede marcar como entregados sus propios despachos. La validacion de estado permite marcar entrega solo desde `pendiente` o `en_ruta`, evitando modificar despachos ya cerrados o en incidencia.

---

## 16. Reporte de incidencia protegido

**Archivo:** `Discopro_Django/apps/motoristas/portal_views.py`  
**Lineas:** 83-99

```83:99:Discopro_Django/apps/motoristas/portal_views.py
@login_required(login_url='usuarios:login')
@motorista_requerido
def reportar_incidencia(request, pk):
    motorista = _motorista_actual(request)
    despacho = get_object_or_404(Movimiento, pk=pk, motorista=motorista)
    if request.method == 'POST':
        despacho.estado = 'incidencia'
        despacho.tipo_incidencia = request.POST.get('tipo_incidencia', '')
        despacho.comentario_incidencia = request.POST.get('comentario_incidencia', '').strip()
        despacho.save(update_fields=['estado', 'tipo_incidencia', 'comentario_incidencia', 'actualizado_en'])
        messages.success(request, 'Incidencia registrada.')
        return redirect('portal_motorista:detalle', pk=despacho.pk)
    return render(request, 'motorista_portal/incidencia.html', {
        'motorista': motorista,
        'despacho': despacho,
        'tipos_incidencia': Movimiento.TIPOS_INCIDENCIA,
    })
```

**Descripcion de seguridad:**  
La incidencia solo se registra sobre un despacho perteneciente al motorista autenticado. La vista evita que un usuario cambie el estado de despachos ajenos usando IDs manipulados en la URL.

---

## 17. Cambio de contrasena con verificacion previa

**Archivo:** `Discopro_Django/apps/usuarios/views.py`  
**Lineas:** 65-87

```65:87:Discopro_Django/apps/usuarios/views.py
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
```

**Descripcion de seguridad:**  
Para cambiar la contrasena, el usuario debe estar autenticado y debe conocer la contrasena actual. `check_password()` valida la contrasena actual usando el hash almacenado. `set_password()` guarda la nueva contrasena hasheada, no en texto plano.

---

## 18. Validadores de contrasena de Django

**Archivo:** `Discopro_Django/discopro/settings.py`  
**Lineas:** 82-95

```82:95:Discopro_Django/discopro/settings.py
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

**Descripcion de seguridad:**  
Estos validadores reducen el uso de contrasenas debiles. Django verifica similitud con datos del usuario, longitud minima, contrasenas comunes y contrasenas solo numericas.

---

## 19. Creacion segura de usuarios motoristas

**Archivo:** `Discopro_Django/apps/motoristas/forms.py`  
**Lineas:** 326-332

```326:332:Discopro_Django/apps/motoristas/forms.py
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data.get('email') or '',
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data.get('first_name', ''),
            last_name=self.cleaned_data.get('last_name', ''),
        )
```

**Descripcion de seguridad:**  
`create_user()` es el metodo recomendado por Django para crear usuarios porque hashea automaticamente la contrasena antes de guardarla. Esto evita almacenar contrasenas en texto plano.

---

## 20. Validacion de duplicados en formularios

**Archivo:** `Discopro_Django/apps/motoristas/forms.py`  
**Lineas:** 308-320

```308:320:Discopro_Django/apps/motoristas/forms.py
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        from apps.usuarios.models import Usuario
        if rut and Usuario.objects.filter(rut=rut).exists():
            raise forms.ValidationError('Este RUT ya está registrado.')
        return rut

    def clean_username(self):
        username = self.cleaned_data.get('username')
        from django.contrib.auth.models import User
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya existe.')
        return username
```

**Descripcion de seguridad:**  
Estas validaciones evitan registrar dos usuarios con el mismo RUT o nombre de usuario. Esto protege la integridad de identidad y reduce conflictos de autenticacion.

---

## 21. Restricciones de unicidad en modelos

**Archivo:** `Discopro_Django/apps/motoristas/models.py`  
**Lineas:** 5-14, 28-30, 68-69

```5:14:Discopro_Django/apps/motoristas/models.py
class Sucursal(models.Model):
    """Farmacia desde donde opera la flota."""
    nombre = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=100, default='')
    provincia = models.CharField(max_length=100, default='')
    comuna = models.CharField(max_length=100, default='')
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    encargado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='sucursales_encargadas')
    activo = models.BooleanField(default=True)
```

```28:30:Discopro_Django/apps/motoristas/models.py
class Moto(models.Model):
    """Modelo para los vehículos (motos)"""
    placa = models.CharField(max_length=20, unique=True)
```

```68:69:Discopro_Django/apps/motoristas/models.py
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='motorista')
    licencia = models.CharField(max_length=20, unique=True)
```

**Descripcion de seguridad:**  
Las restricciones `unique=True` impiden duplicados a nivel de base de datos. Esto protege la integridad de datos: una farmacia no se duplica por nombre, una moto no se duplica por placa y una licencia no se repite entre motoristas.

---

## 22. Numero de despacho unico e indices

**Archivo:** `Discopro_Django/apps/movimientos/models.py`  
**Lineas:** 21-24 y 32-40

```21:24:Discopro_Django/apps/movimientos/models.py
    numero_despacho = models.CharField(max_length=50, unique=True)
    direccion_destino = models.CharField(max_length=255, default='')
    motorista = models.ForeignKey(Motorista, on_delete=models.SET_NULL, null=True, blank=True, related_name='despachos')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True, related_name='despachos')
```

```32:40:Discopro_Django/apps/movimientos/models.py
    class Meta:
        db_table = 'movimiento'
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['-creado_en']
        indexes = [
            models.Index(fields=['numero_despacho']),
            models.Index(fields=['motorista', 'estado']),
        ]
```

**Descripcion de seguridad:**  
`numero_despacho` es unico, evitando registrar dos movimientos con el mismo codigo. Los indices ayudan a consultar rapidamente por numero de despacho, motorista y estado, reduciendo errores y mejorando trazabilidad.

---

## 23. Validacion al crear movimientos

**Archivo:** `Discopro_Django/discopro/urls.py`  
**Lineas:** 153-181

```153:181:Discopro_Django/discopro/urls.py
def _crear_movimiento_desde_post(request):
    numero_despacho = request.POST.get('numero_despacho', '').strip()
    direccion_destino = request.POST.get('direccion_destino', '').strip()
    motorista_id = request.POST.get('motorista')

    if not numero_despacho or not direccion_destino or not motorista_id:
        messages.error(request, 'Complete todos los campos obligatorios.')
        return False

    if Movimiento.objects.filter(numero_despacho=numero_despacho).exists():
        messages.error(request, 'El número de despacho ya existe.')
        return False

    motorista = Motorista.objects.select_related('sucursal').filter(pk=motorista_id, activo=True).first()
    if motorista is None:
        messages.error(request, 'Seleccione un motorista válido.')
        return False
    if motorista.sucursal is None:
        messages.error(request, 'El motorista seleccionado no tiene farmacia asignada.')
        return False

    Movimiento.objects.create(
        numero_despacho=numero_despacho,
        direccion_destino=direccion_destino,
        motorista=motorista,
        sucursal=motorista.sucursal,
    )
    messages.success(request, 'Movimiento registrado exitosamente.')
    return True
```

**Descripcion de seguridad:**  
Antes de crear un movimiento, el codigo valida campos obligatorios, evita duplicidad de `numero_despacho`, exige que el motorista exista y que este activo, y verifica que tenga farmacia asignada. Esto evita registros incompletos o asignaciones invalidas.

Tambien se usa ORM (`filter`, `create`) en lugar de SQL manual, reduciendo riesgo de inyeccion SQL.

---

## 24. Dashboard protegido por autenticacion

**Archivo:** `Discopro_Django/discopro/urls.py`  
**Lineas:** 184-192

```184:192:Discopro_Django/discopro/urls.py
@login_required(login_url='usuarios:login')

def home(request):

    motoristas = Motorista.objects.filter(activo=True).select_related('usuario__user', 'moto', 'sucursal')

    movimientos = Movimiento.objects.select_related('motorista__usuario__user', 'motorista__moto', 'sucursal').order_by('-creado_en')

    movimientos = filtrar_movimientos(movimientos, request.GET)
```

**Descripcion de seguridad:**  
El dashboard principal requiere usuario autenticado. Las consultas se hacen con el ORM de Django, lo que evita construir SQL con cadenas manuales. Ademas, los motoristas listados se filtran por `activo=True`.

---

## 25. Seguridad en la interfaz segun rol

**Archivo:** `Discopro_Django/apps/usuarios/context_processors.py`  
**Lineas:** 4-10

```4:10:Discopro_Django/apps/usuarios/context_processors.py
def permisos_usuario(request):
    user = request.user
    return {
        'user_rol': obtener_rol(user) if user.is_authenticated else None,
        'es_operador': es_operador(user) if user.is_authenticated else False,
        'puede_gestionar_flota': puede_gestionar_flota(user) if user.is_authenticated else False,
    }
```

**Archivo:** `Discopro_Django/templates/base.html`  
**Lineas:** 28-40

```28:40:Discopro_Django/templates/base.html
                    {% if user_rol == 'motorista' %}
                    <li><a href="{% url 'portal_motorista:inicio' %}"><i class="fa-solid fa-house"></i> Inicio</a></li>
                    <li><a href="{% url 'portal_motorista:mis_despachos' %}"><i class="fa-solid fa-route"></i> Mis despachos</a></li>
                    <li><a href="{% url 'portal_motorista:perfil' %}"><i class="fa-solid fa-user"></i> Mi perfil</a></li>
                    <li><a href="{% url 'portal_motorista:mi_moto' %}"><i class="fa-solid fa-motorcycle"></i> Mi moto</a></li>
                    <li><a href="{% url 'portal_motorista:historial' %}"><i class="fa-solid fa-clock-rotate-left"></i> Historial</a></li>
                    {% else %}
                    <li><a href="{% url 'home' %}"><i class="fa-solid fa-truck-fast"></i> Movimientos</a></li>
                    {% if puede_gestionar_flota %}
                    <li><a href="{% url 'farmacia:lista' %}"><i class="fa-solid fa-store"></i> Farmacias</a></li>
                    <li><a href="{% url 'motoristas:lista' %}"><i class="fa-solid fa-people"></i> Motoristas</a></li>
                    {% endif %}
                    {% endif %}
```

**Descripcion de seguridad:**  
El menu se adapta al rol del usuario. Un motorista ve solo opciones de su portal; un administrador o despachador ve opciones de flota. Esta proteccion visual mejora la experiencia y reduce errores, pero debe complementarse con decoradores en las vistas, como efectivamente ocurre en el servidor.

---

## 26. API REST solo para usuarios autenticados

**Archivo:** `Discopro_Django/discopro/settings.py`  
**Lineas:** 111-120

```111:120:Discopro_Django/discopro/settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

**Archivo:** `Discopro_Django/apps/api/views.py`  
**Lineas:** 52-55

```52:55:Discopro_Django/apps/api/views.py
class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated]
```

**Descripcion de seguridad:**  
La API REST usa `SessionAuthentication` y exige `IsAuthenticated`. Esto significa que los endpoints bajo `/api/` no deben responder datos a usuarios anonimos. Cada ViewSet tambien declara `permission_classes = [permissions.IsAuthenticated]`, reforzando la regla.

---

## 27. CORS restringido a origenes conocidos

**Archivo:** `Discopro_Django/discopro/settings.py`  
**Lineas:** 123-128

```123:128:Discopro_Django/discopro/settings.py
# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
```

**Descripcion de seguridad:**  
CORS define que origenes externos pueden hacer solicitudes desde navegador hacia la aplicacion. En este caso se permiten solo origenes locales usados en desarrollo. Esto evita dejar la API abierta a cualquier dominio desde peticiones cross-origin.

---

## 28. Registro de eventos del sistema

**Archivo:** `Discopro_Django/discopro/settings.py`  
**Lineas:** 130-145

```130:145:Discopro_Django/discopro/settings.py
# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'discopro.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

**Descripcion de seguridad:**  
El logging permite registrar eventos del sistema en `logs/discopro.log`. Esto ayuda a revisar comportamiento de la aplicacion, diagnosticar errores y mantener trazabilidad.

---

## 29. Resumen de patrones encontrados

| Patron de seguridad | Archivo principal | Lineas |
|---|---|---|
| Variables de entorno para secretos | `discopro/settings.py` | 14-16 |
| Middleware de seguridad | `discopro/settings.py` | 36-45 |
| CSRF | `settings.py` / `templates/login.html` | 41 / 124-125 |
| Autenticacion con Django Auth | `apps/usuarios/views.py` | 18-43 |
| Redireccion por rol | `apps/usuarios/views.py` | 10-16 |
| Logout seguro | `apps/usuarios/views.py` | 46-51 |
| `@login_required` | `apps/motoristas/portal_views.py` | 27-29 |
| RBAC | `apps/usuarios/permissions.py` | 9-37 |
| Portal exclusivo motorista | `apps/motoristas/portal_views.py` | 11-17 |
| Anti-IDOR | `apps/motoristas/portal_views.py` | 50-55, 58-87 |
| Cambio de contrasena seguro | `apps/usuarios/views.py` | 65-87 |
| Validadores de contrasena | `discopro/settings.py` | 82-95 |
| Creacion segura de usuarios | `apps/motoristas/forms.py` | 326-332 |
| Validacion de duplicados | `apps/motoristas/forms.py` | 308-320 |
| Restricciones `unique=True` | `models.py` | varias |
| Validacion al crear movimiento | `discopro/urls.py` | 153-181 |
| UI segun rol | `context_processors.py` / `base.html` | 4-10 / 28-40 |
| API autenticada | `settings.py` / `apps/api/views.py` | 111-120 / 52-55 |
| CORS | `discopro/settings.py` | 123-128 |
| Logging | `discopro/settings.py` | 130-145 |

---

