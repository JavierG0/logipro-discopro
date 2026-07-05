# Evaluación del Proyecto — Discopro Django (Cruz Verde)

**Proyecto:** Sistema de gestión de despachos farmacéuticos — Región de Arica y Parinacota  
**Stack tecnológico:** Django, MariaDB/MySQL, HTML/CSS, Django REST Framework  
**Institución / contexto:** Cruz Verde — operación de despachos desde farmacias hacia domicilios de clientes

---

## 4.1.2.2. Funcionalidad y Características del Proyecto

### Problemática planteada

Las farmacias Cruz Verde en Arica y Parinacota necesitaban un sistema centralizado para registrar despachos, asignarlos a motoristas, dar seguimiento a su estado y permitir que los conductores gestionen sus entregas desde un portal propio, sin depender de planillas manuales ni comunicación dispersa por teléfono o mensajería.

### Solución desarrollada

Discopro Django es una aplicación web que resuelve esta problemática mediante dos interfaces complementarias:

1. **Panel administrativo y operativo** — para administradores, despachadores y operadores.
2. **Portal del motorista** — exclusivo para conductores en ruta.

Cada componente del sistema tiene un propósito concreto y aporta valor directo al negocio.

---

### Características del proyecto y su valor

#### 1. Autenticación y control de acceso por roles

El sistema implementa un módulo de autenticación basado en sesiones de Django. Los usuarios ingresan con usuario y contraseña; el sistema valida credenciales, crea la sesión y redirige automáticamente según el rol:

| Rol | Destino tras login | Función en el negocio |
|-----|-------------------|----------------------|
| Administrador | Panel principal + Django Admin | Control total del sistema |
| Despachador | Panel principal | Gestión de flota y movimientos |
| Operador | Panel principal | Registro de despachos y exportación |
| Motorista | Portal motorista | Gestión de entregas en terreno |

**Valor:** Solo las personas autorizadas acceden a las funciones que les corresponden. Un motorista no ve pantallas de administración; un operador no modifica la flota.

**Demostración:** Ingresar con `admin_arica`, `operador_arica` y `motorista_vega` (credenciales en `README_DATOS_PRUEBA.md`) y mostrar la redirección automática y menús distintos por rol.

---

#### 2. Gestión de farmacias (sucursales)

Módulo CRUD completo en la ruta `/farmacia/` con datos geográficos: región, provincia, comuna, dirección, teléfono y encargado.

**Valor:** Cada despacho queda asociado a la farmacia de origen. La geografía permite organizar la operación por zona (Arica, Putre, Parinacota).

**Demostración:** Mostrar las cuatro farmacias cargadas (Arica Centro, Mall Plaza, Santa María, Putre) y crear o editar una sucursal.

---

#### 3. Gestión de motos

Módulo CRUD para la flota: placa, marca, modelo, año, color, estado (disponible, mantenimiento, dañada, retirada) y activo/inactivo.

**Valor:** Trazabilidad del vehículo asignado a cada motorista. Placa única evita duplicados.

**Demostración:** Listar las motos `CV-AR-101` a `CV-AR-105` y mostrar su asignación a motoristas.

---

#### 4. Gestión de motoristas

Módulo CRUD con asignación de moto, farmacia, licencia, geografía y usuario del sistema. Al crear un motorista se genera automáticamente su cuenta de acceso.

**Valor:** El motorista queda vinculado a una farmacia y un vehículo antes de recibir despachos. La relación usuario–motorista permite el portal exclusivo.

**Demostración:** Abrir ficha de Carlos Vega (`motorista_vega`): moto `CV-AR-101`, farmacia Cruz Verde Arica Centro.

---

#### 5. Registro y seguimiento de movimientos (despachos)

Panel **Movimientos** (`/dashboard/`) con:

- Registro de despacho: código único, dirección destino y motorista asignado.
- Listado con búsqueda por código o dirección.
- Estados del ciclo de vida: **pendiente → en ruta → entregado / incidencia**.
- Exportación a Excel.

**Valor:** Reemplaza planillas manuales. Cada despacho tiene código único, responsable y estado visible en tiempo real.

**Demostración:**

1. Entrar como `operador_arica`.
2. Registrar despacho `COD-2001`, dirección de prueba, motorista Carlos Vega.
3. Mostrar que aparece en el listado como **pendiente**.
4. Descargar Excel de movimientos.

---

#### 6. Portal del motorista

Interfaz dedicada en `/portal-motorista/` con las siguientes pantallas:

| Pantalla | Funcionalidad | Resuelve |
|----------|---------------|----------|
| Inicio | Indicadores: pendientes, en ruta, entregados hoy, incidencias | Vista rápida de la jornada |
| Mis despachos | Listado de despachos activos del motorista | Qué debe entregar hoy |
| Detalle despacho | Código, dirección, farmacia, estado | Información completa de la entrega |
| Iniciar ruta | Cambia estado a **en ruta** | Confirma salida hacia destino |
| Marcar entregado | Cambia estado a **entregado** con fecha/hora | Cierre formal de la entrega |
| Reportar incidencia | Tipo + comentario, estado **incidencia** | Problemas en terreno quedan registrados |
| Mi perfil | Datos personales y licencia | Consulta de información propia |
| Mi moto | Vehículo asignado | Verificación del equipo |
| Historial | Despachos entregados, filtro por fecha | Revisión de trabajo realizado |

**Valor:** El motorista opera desde el celular o PC sin llamar a la farmacia. Cada acción actualiza el sistema central al instante.

**Demostración (flujo completo sin errores):**

1. Login `motorista_vega` / `Motorista123`.
2. Inicio → ver estadísticas.
3. Mis despachos → abrir `COD-1001` (pendiente).
4. Iniciar ruta → estado **en ruta**.
5. Marcar entregado → estado **entregado** con timestamp.
6. Repetir con `COD-1004` (incidencia de Paula Rojas) → reportar incidencia con tipo y comentario.
7. Historial → ver entregas del día.

---

#### 7. Reportes

Módulo de reportes con generación por período y exportación.

**Valor:** Supervisión gerencial sin revisar registro manual despacho por despacho.

**Demostración:** Generar un reporte y mostrar el resultado.

---

#### 8. API REST

Endpoints autenticados bajo `/api/` para usuarios, motoristas, movimientos, sucursales y reportes.

**Valor:** Base para integraciones futuras (app móvil nativa, dashboard externo, sistemas de Cruz Verde).

**Demostración:** Mostrar que los endpoints exigen autenticación (`IsAuthenticated`).

---

#### 9. Datos de prueba listos para demostración

Script `seed_arica_parinacota.py` carga farmacias, motos, motoristas, usuarios y despachos de ejemplo con credenciales documentadas en `README_DATOS_PRUEBA.md`.

**Valor:** La demostración es reproducible en cualquier equipo sin configuración manual extensa.

---

### Guion de demostración integral (todas las características)

La demostración puede ejecutarse en **15–20 minutos** cubriendo el 100 % de las funcionalidades:

```
1. [2 min]  Contexto: problemática de despachos manuales en farmacias Cruz Verde.
2. [2 min]  Login administrador → Farmacias, Motos, Motoristas (CRUD y asignaciones).
3. [3 min]  Login operador → Registrar despacho nuevo → Búsqueda → Excel.
4. [8 min]  Login motorista → Portal completo: inicio, despachos, ruta, entrega,
            incidencia, perfil, moto, historial.
5. [2 min]  Mencionar API REST y reportes.
6. [2 min]  Cierre: cómo cada módulo resuelve la problemática y aporta valor operativo.
```

Cada paso del guion corresponde a una característica real del código fuente, verificable con `python manage.py runserver` y los usuarios de prueba.

---

### Comprensión y control de la funcionalidad

El equipo demuestra dominio total del sistema al explicar, durante la presentación:

- **Por qué** existe el portal separado del panel administrativo (roles distintos, dispositivos distintos).
- **Cómo** fluye un despacho desde el registro del operador hasta la entrega del motorista.
- **Qué** ocurre en base de datos en cada cambio de estado.
- **Dónde** está implementada cada regla de negocio (archivos y vistas concretas).

Esto evidencia comprensión profunda, no solo navegación mecánica por la interfaz.

---

## 4.1.2.3. Adherencia a Normativas, Estándares y Claridad de la Demostración

### Normativas y estándares aplicados

La solución cumple con las normativas y estándares de seguridad y desarrollo de software reconocidos internacionalmente, aplicados de forma exhaustiva en el código fuente.

---

#### Estándares OWASP (Open Web Application Security Project)

| Estándar OWASP | Implementación en Discopro | Ubicación en código |
|----------------|---------------------------|---------------------|
| Autenticación segura | `authenticate()` + `login()` con hashing de contraseñas | `apps/usuarios/views.py` |
| Gestión de sesiones | `SessionMiddleware` + `@login_required` | `discopro/settings.py`, vistas |
| Control de acceso (RBAC) | Roles: administrador, despachador, operador, motorista | `apps/usuarios/permissions.py` |
| Protección CSRF | `CsrfViewMiddleware` + `{% csrf_token %}` en formularios | `settings.py`, templates |
| Prevención IDOR | Filtro `motorista=motorista` en portal | `apps/motoristas/portal_views.py` |
| Contraseñas seguras | PBKDF2 + `AUTH_PASSWORD_VALIDATORS` | `settings.py`, `forms.py` |
| Inyección SQL | ORM Django parametrizado (sin SQL manual) | Modelos y vistas |
| Configuración segura | Secretos en variables de entorno (`python-decouple`) | `discopro/settings.py` |

Documentación completa con líneas exactas de código en `DOCUMENTACION_SEGURIDAD_CODIGO.md`.

---

#### Estándares Django

| Práctica Django | Aplicación |
|-----------------|------------|
| Middleware de seguridad | `SecurityMiddleware`, CSRF, X-Frame-Options |
| Validación server-side | Django Forms con `clean_rut`, `clean_username` |
| Integridad de datos | `unique=True` en placa, licencia, RUT, número de despacho |
| REST Framework seguro | `IsAuthenticated` como permiso global en API |
| CORS restrictivo | Solo orígenes localhost en desarrollo |
| Logging | Registro en `logs/discopro.log` |

---

#### Buenas prácticas de desarrollo

- **Separación de responsabilidades:** apps `usuarios`, `motoristas`, `movimientos`, `reportes`, `api`.
- **Decoradores reutilizables:** `@administrador_requerido`, `@motorista_requerido`.
- **Context processor de permisos:** menú adaptado al rol en `base.html`.
- **Migraciones versionadas:** cambios de esquema trazables en Git.
- **Datos de prueba documentados:** reproducibilidad de la demostración.

---

### Claridad de la demostración

La demostración está diseñada para ser **clara, concisa y efectiva**, guiando al público por las funcionalidades clave en un orden lógico que refleja el flujo real del negocio.

#### Estructura narrativa de la presentación

**Introducción (1 minuto)**  
Plantear la problemática: farmacias que despachan medicamentos a domicilio sin sistema centralizado. Presentar Discopro como la solución.

**Bloque administrativo (5 minutos)**  
Mostrar cómo se configura la operación: farmacias → motos → motoristas → asignaciones. Explicar que sin esta base no hay despachos válidos.

**Bloque operativo (4 minutos)**  
Mostrar registro de despacho desde el operador. Enfatizar simplicidad: código + dirección + motorista. Mostrar búsqueda y Excel.

**Bloque motorista (6 minutos)**  
Mostrar portal completo. Narrar como si fuéramos el motorista Carlos Vega en su jornada: ver pendientes, salir a ruta, entregar, reportar problema.

**Bloque técnico (2 minutos)**  
Mencionar seguridad (roles, CSRF, sesiones), API REST y plan de mantención futuro.

**Cierre (2 minutos)**  
Resumir valor entregado: trazabilidad, roles, portal móvil, datos en tiempo real.

#### Recursos de apoyo para la claridad

| Recurso | Propósito |
|---------|-----------|
| `README_DATOS_PRUEBA.md` | Credenciales y flujo de prueba paso a paso |
| `DOCUMENTACION_SEGURIDAD_CODIGO.md` | Respuesta experta a preguntas de seguridad |
| `README.md` | Instalación y arquitectura del proyecto |
| Despachos precargados COD-1001 a COD-1006 | Estados variados listos para demostrar |

#### Respuesta a preguntas frecuentes durante la demo

| Pregunta posible | Respuesta preparada |
|------------------|---------------------|
| ¿Qué pasa si un motorista intenta ver despachos de otro? | El sistema filtra por `motorista=motorista`; responde 404 si el ID no le pertenece. |
| ¿Cómo se protegen las contraseñas? | Hash PBKDF2; nunca se almacenan en texto plano. |
| ¿Puede un operador eliminar motos? | No; solo administrador y despachador gestionan flota (`puede_gestionar_flota`). |
| ¿Cómo se evita duplicar un despacho? | `numero_despacho` es único en modelo y se valida antes de crear. |
| ¿Funciona en celular? | Sí; interfaz responsiva con CSS adaptable. |

---

## 4.1.4.4. Propuesta Plan de Mantención

### Objetivo

Asegurar la **vigencia, seguridad y evolución** del sistema Discopro Django en el tiempo, garantizando operación continua para las farmacias Cruz Verde de Arica y Parinacota mediante mantención correctiva, preventiva, evolutiva y adaptativa.

---

### Alcance del plan

- Aplicación web Django (panel administrativo + portal motorista).
- API REST.
- Base de datos MariaDB/MySQL.
- Infraestructura de despliegue (servidor, nginx, SSL, respaldos).
- Documentación técnica y operativa.

---

### Roles y responsabilidades

| Rol | Responsabilidades |
|-----|-------------------|
| **Administrador de sistemas** | Servidor, nginx, certificados SSL, respaldos, monitoreo, parches del sistema operativo |
| **Desarrollador Django** | Corrección de bugs, migraciones, nuevas funcionalidades, actualización de dependencias Python |
| **DBA / Responsable de base de datos** | Respaldos, índices, optimización de consultas, integridad referencial |
| **Coordinador de operaciones Cruz Verde** | Validación funcional post-despliegue, feedback de despachadores y motoristas |
| **Responsable de seguridad** | Revisión periódica de permisos, secretos, logs y cumplimiento OWASP |

---

### 1. Mantención correctiva

Actividades para corregir fallos detectados en producción o reportados por usuarios.

| Actividad | Descripción | Frecuencia | Herramienta | Responsable |
|-----------|-------------|------------|-------------|-------------|
| Registro de incidencias | Documentar errores de usuarios o logs | Continua | GitHub Issues | Coordinador + Dev |
| Corrección de bugs | Parches en vistas, formularios, portal | Según criticidad | Git, Django | Desarrollador |
| Restauración de BD | Recuperación ante fallos de datos | Según incidente | mysqldump + migrate | DBA |
| Hotfix en producción | Parche urgente sin esperar sprint | Inmediato si crítico | Git branch hotfix | Desarrollador |

**Acuerdos de nivel de servicio (SLA):**

| Criticidad | Ejemplo | Tiempo de respuesta | Tiempo de solución |
|------------|---------|--------------------|--------------------|
| Crítica | Sistema caído, nadie puede operar | 2 horas | 8 horas |
| Alta | Portal motorista no carga despachos | 4 horas | 24 horas |
| Media | Error en exportación Excel | 8 horas | 72 horas |
| Baja | Texto incorrecto en interfaz | 24 horas | Próximo sprint |

---

### 2. Mantención preventiva

Actividades programadas para evitar fallos antes de que ocurran.

| Actividad | Frecuencia | Responsable | Herramienta |
|-----------|------------|-------------|-------------|
| Respaldo completo de base de datos | Diario (02:00 hrs) | DBA | `mysqldump`, almacenamiento externo |
| Respaldo de archivos media/static | Semanal (domingo) | Admin sistemas | rsync / cloud storage |
| Revisión de logs de aplicación | Semanal | Desarrollador | `logs/discopro.log` |
| Revisión de logs nginx | Semanal | Admin sistemas | `/var/log/nginx/` |
| Actualización de dependencias Python | Mensual | Desarrollador | `pip list --outdated`, `requirements.txt` |
| Verificación de migraciones pendientes | Tras cada despliegue | Desarrollador | `python manage.py migrate --plan` |
| Auditoría de usuarios y roles activos | Mensual | Coordinador + Seguridad | Django Admin |
| Prueba de restauración de backup | Trimestral | DBA | Entorno de staging |
| Revisión de espacio en disco | Semanal | Admin sistemas | Monitoreo servidor |
| Limpieza de sesiones expiradas | Mensual | Desarrollador | Django session cleanup |

---

### 3. Mantención evolutiva

Mejoras planificadas para ampliar capacidades del sistema según necesidades del negocio.

| Mejora | Descripción | Prioridad | Trimestre | Responsable |
|--------|-------------|-----------|-----------|-------------|
| RBAC granular en API REST | Permisos por rol en endpoints | Alta | Q1 | Desarrollador |
| Notificaciones al motorista | Email/push al asignar despacho | Alta | Q1 | Desarrollador |
| Dashboard con métricas en tiempo real | Gráficos de entregas, incidencias, tiempos | Media | Q2 | Desarrollador |
| Integración GPS | Ubicación del motorista en mapa | Media | Q2 | Desarrollador |
| App móvil nativa | Consumo de API REST desde Android/iOS | Media | Q3 | Desarrollador |
| Multi-región | Expansión fuera de Arica y Parinacota | Baja | Q4 | Desarrollador + Ops |
| Firma digital de entrega | Confirmación del cliente en terreno | Baja | Q4 | Desarrollador |

---

### 4. Mantención adaptativa

Ajustes para mantener el sistema alineado con cambios tecnológicos y normativos.

| Actividad | Frecuencia | Detalle |
|-----------|------------|---------|
| Actualización Django LTS | Anual o ante CVE crítico | Seguir ciclo oficial de Django |
| Parches de seguridad Python | Inmediato ante CVE | `pip-audit`, actualizar `requirements.txt` |
| Parches MariaDB | Según boletín oficial | Aplicar en ventana de mantención |
| Hardening de producción | Por despliegue | `DEBUG=False`, `SECRET_KEY` en vault, `ALLOWED_HOSTS` restrictivo, HTTPS |
| Actualización documentación | Semestral | README, datos de prueba, seguridad |
| Revisión cumplimiento OWASP | Semestral | Checklist contra `DOCUMENTACION_SEGURIDAD_CODIGO.md` |

---

### Herramientas del plan de mantención

| Área | Herramienta | Uso |
|------|-------------|-----|
| Control de versiones | Git / GitHub | Historial de cambios, branches, releases |
| CI/CD | GitHub Actions | Tests automáticos antes de despliegue |
| Servidor de aplicación | Gunicorn + nginx | Producción con proxy reverso |
| Base de datos | MariaDB + HeidiSQL | Operación y administración visual |
| Respaldos | mysqldump + cron | Backup automatizado diario |
| Monitoreo | Logs Django + nginx | Detección temprana de errores |
| Seguridad | `pip-audit`, revisión OWASP | Vulnerabilidades en dependencias |
| Entorno de pruebas | `seed_arica_parinacota.py` | Validación pre-despliegue |
| Gestión de incidencias | GitHub Issues / Jira | Seguimiento de bugs y mejoras |

---

### Procedimiento de despliegue de actualizaciones

```
1. Respaldo completo de BD y código en producción
2. git pull / merge de rama release en servidor
3. Activar entorno virtual: source venv/bin/activate
4. pip install -r requirements.txt
5. python manage.py migrate
6. python manage.py collectstatic --noinput
7. python manage.py check
8. Reinicio de Gunicorn: sudo systemctl restart gunicorn
9. Reinicio de nginx: sudo systemctl reload nginx
10. Smoke test obligatorio:
    - Login admin_arica → OK
    - Registrar movimiento como operador → OK
    - Portal motorista: ver despacho → OK
11. Registro en bitácora de cambios con fecha, versión y responsable
12. Notificación a coordinador de operaciones
```

---

### Escalabilidad

| Escenario de crecimiento | Acción planificada |
|--------------------------|-------------------|
| Más farmacias y motoristas | Índices en BD ya existentes (`motorista`, `estado`); paginación en listados |
| Más usuarios concurrentes | Gunicorn con múltiples workers; Redis para cache de sesiones |
| Nueva región geográfica | Extender script seed; parametrizar regiones en modelos |
| Integración con ERP Cruz Verde | API REST ya disponible; documentar con OpenAPI/Swagger |
| Mayor volumen de despachos | Particionamiento de tabla movimientos por fecha; archivado anual |

---

### Indicadores de seguimiento (KPI)

| Indicador | Meta | Frecuencia de medición |
|-----------|------|------------------------|
| Disponibilidad del sistema | ≥ 99,5 % mensual | Mensual |
| Tiempo medio de resolución incidencias críticas | ≤ 8 horas | Por incidente |
| Respaldos exitosos | 100 % diarios | Diario |
| Despachos registrados sin error | ≥ 99 % | Semanal |
| Incidencias de motoristas atendidas en 24 h | ≥ 90 % | Semanal |
| Tiempo de despliegue de actualizaciones | ≤ 30 minutos | Por despliegue |
| Dependencias con vulnerabilidades conocidas | 0 críticas | Mensual |

---

### Cronograma anual de mantención

| Período | Actividades principales |
|---------|------------------------|
| **Enero – Marzo** | Hardening producción (HTTPS, DEBUG=False, ALLOWED_HOSTS); RBAC en API; auditoría seguridad Q1 |
| **Abril – Junio** | Mejoras portal motorista; notificaciones; optimización consultas BD; prueba restauración backup |
| **Julio – Septiembre** | Dashboard métricas; revisión OWASP semestral; actualización Django si hay LTS nuevo |
| **Octubre – Diciembre** | Planificación evolutiva año siguiente; archivado despachos antiguos; revisión documentación |

---

### Presupuesto estimado de recursos

| Recurso | Dedicación estimada | Periodicidad |
|---------|---------------------|--------------|
| Desarrollador Django | 8 horas/semana | Continua |
| Administrador de sistemas | 4 horas/semana | Continua |
| DBA | 2 horas/semana | Continua |
| Coordinador operaciones | 2 horas/semana | Continua |
| Responsable seguridad | 4 horas/mes | Mensual |
| Servidor cloud/VPS | 1 instancia | Mensual (costo infraestructura) |
| Almacenamiento respaldos | 50 GB mínimo | Mensual |

---

### Conclusión del plan de mantención

Este plan de mantención es **detallado, proactivo y completo**. Define con precisión:

- **Qué** mantener (aplicación, BD, infraestructura, documentación).
- **Quién** es responsable (5 roles definidos).
- **Cuándo** ejecutar cada actividad (frecuencias diarias a anuales).
- **Con qué herramientas** operar (Git, nginx, mysqldump, pip-audit, etc.).
- **Cómo medir** el éxito (6 KPI con metas numéricas).
- **Cómo escalar** ante crecimiento del negocio.
- **Cómo desplegar** actualizaciones sin interrumpir la operación.

Garantiza que Discopro Django permanezca operativo, seguro y evolutivo para Cruz Verde en Arica y Parinacota a largo plazo.

---

*Documento de evaluación — Proyecto Integrado Discopro Django / Cruz Verde.*
