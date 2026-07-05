# Plan de Mantención — Discopro Django (Cruz Verde)

**Sistema:** Gestión de despachos farmacéuticos
**Entorno actual:** Desarrollo y demostración local (Visual Studio Code, `python manage.py runserver`, base de datos MariaDB/MySQL en localhost)

---

## Introducción

Este plan de mantención describe cómo conservar operativa, segura y evolutiva la solución Discopro Django en el tiempo. Está redactado según el **contexto real del proyecto**: la aplicación se ejecuta en entorno local desde VS Code, no existe actualmente un servidor de producción con Gunicorn, nginx ni métricas de CPU. Por eso, las frecuencias y recursos se plantean de forma **proporcional y realista**, dejando indicado qué cambiaría si el sistema pasara a un despliegue formal en el futuro.

El plan se organiza **según quién ejecuta cada mantención**, para que cada responsable sepa exactamente qué le corresponde.

---

## Mantención a cargo del desarrollador

El desarrollador es quien mantiene el código fuente, las dependencias Python, las migraciones de base de datos y la corrección de errores funcionales. En el entorno actual, esto implica trabajar directamente sobre el proyecto abierto en VS Code.

### Resolución de errores (mantención correctiva)

Cuando un usuario de prueba —administrador, operador o motorista— reporta que algo no funciona, el desarrollador reproduce el error en local activando el servidor con `python manage.py runserver`, revisa la traza en la terminal de VS Code y consulta, si es necesario, el archivo `logs/discopro.log`. Los errores se registran en el repositorio Git (por ejemplo, como issue en GitHub) indicando qué rol estaba afectado, qué pantalla falló y qué pasos permiten reproducir el problema.

Los fallos se clasifican por impacto. Un error que impide iniciar sesión o registrar despachos se atiende de inmediato. Un problema menor, como un texto incorrecto en una etiqueta, puede resolverse en la siguiente sesión de trabajo. Tras corregir el código, el desarrollador ejecuta `python manage.py check` para verificar que Django no detecte problemas de configuración y prueba manualmente el flujo afectado con los usuarios documentados en `README_DATOS_PRUEBA.md`.

### Actualización de dependencias y del framework

Las librerías del proyecto están listadas en `requirements.txt`. Periódicamente —por ejemplo, al inicio de cada mes o antes de una entrega— conviene revisar si existen versiones nuevas de Django, Django REST Framework u otras dependencias. En local basta con actualizar el entorno virtual, ejecutar `pip install -r requirements.txt` y comprobar que la aplicación sigue funcionando: login, registro de movimientos y portal del motorista.

Si una actualización introduce cambios en migraciones, el desarrollador ejecuta `python manage.py migrate` y verifica que los datos de prueba cargados con `seed_arica_parinacota.py` sigan siendo coherentes.

### Migraciones y modelo de datos

Cada vez que se modifica un modelo en `apps/motoristas/models.py`, `apps/movimientos/models.py` u otras apps, el desarrollador genera migraciones con `python manage.py makemigrations` y las aplica con `python manage.py migrate`. Antes de aplicar cambios estructurales sobre una base de datos con datos reales, se recomienda exportar un respaldo con las herramientas de MariaDB (por ejemplo, desde HeidiSQL o con un volcado manual). En desarrollo, si algo sale mal, se puede recrear la base ejecutando de nuevo el script seed.

### Mantención evolutiva del código

La evolución del sistema —nuevas pantallas, mejoras en el portal del motorista, permisos más finos en la API, eliminación de código duplicado en `discopro/urls.py`— es responsabilidad del desarrollador. Cada mejora debe probarse en local con al menos un usuario de cada rol antes de considerarse estable. Las mejoras prioritarias identificadas para el proyecto incluyen reforzar el control de acceso en la API REST, mejorar validaciones en vistas administrativas y mantener alineada la documentación (`README.md`, `README_DATOS_PRUEBA.md`, `DOCUMENTACION_SEGURIDAD_CODIGO.md`) con el comportamiento real del código.

### Optimización de consultas

Aunque no se dispone de métricas de CPU ni de herramientas de profiling en producción, el desarrollador puede revisar periódicamente que las consultas frecuentes usen el ORM de forma eficiente: `select_related` en listados de movimientos y motoristas, filtros por `activo=True`, y aprovechamiento de los índices ya definidos en el modelo `Movimiento` (`numero_despacho`, `motorista` + `estado`). Si en el futuro el volumen de despachos crece, estas revisiones permitirán escalar sin rediseñar la aplicación.

---

## Mantención a cargo del administrador de base de datos (DBA)

En el contexto actual del proyecto, el rol de DBA puede ser asumido por el mismo desarrollador o por quien administre MariaDB/MySQL en la máquina local. No hay un servidor remoto dedicado; la base de datos corre en localhost.

### Respaldos de la base de datos

Antes de aplicar migraciones importantes, actualizar dependencias mayores o modificar datos masivamente, se debe respaldar la base `discopro_db`. Esto puede hacerse desde HeidiSQL (exportar base de datos o tabla) o mediante un volcado SQL manual. En un entorno de desarrollo, conviene guardar al menos una copia antes de cada hito del proyecto (entrega, demo, evaluación). Si el respaldo falla o la base queda inconsistente, se puede reconstruir el entorno ejecutando migraciones desde cero y volviendo a cargar `seed_arica_parinacota.py`.

### Integridad de los datos

El DBA —o quien cumpla esa función— verifica que las restricciones del modelo se respeten: números de despacho únicos, placas de moto únicas, licencias de motorista únicas y RUT de usuario único. Estas reglas ya están definidas en los modelos con `unique=True`; la mantención consiste en revisar periódicamente que no existan registros huérfanos o inconsistencias (por ejemplo, motoristas activos sin farmacia asignada, despachos sin motorista).

### Limpieza y orden de la base de datos

En desarrollo, los datos de prueba pueden acumularse. Periódicamente se puede limpiar la base y volver a ejecutar el seed para mantener un estado conocido y reproducible para demostraciones. Si en el futuro el sistema pasa a producción, aquí se planificaría el archivado de despachos antiguos; por ahora, basta con documentar cuándo se regeneraron los datos de prueba.

---

## Mantención a cargo del responsable de seguridad

La seguridad del proyecto no depende de un servidor externo, sino de cómo está configurado y documentado el código. El responsable de seguridad —que puede ser el mismo integrante del equipo con foco en buenas prácticas— revisa que los patrones descritos en `DOCUMENTACION_SEGURIDAD_CODIGO.md` sigan vigentes tras cada cambio relevante.

### Revisión de autenticación y roles

Se verifica que el login siga usando `authenticate()` y `login()` de Django, que las vistas sensibles mantengan `@login_required`, y que los decoradores `@administrador_requerido` y `@motorista_requerido` sigan aplicados en las rutas correspondientes. También se comprueba que un motorista no pueda acceder a despachos ajenos comprobando el filtro `motorista=motorista` en `portal_views.py`.

### Revisión de CSRF y contraseñas

Todos los formularios POST deben seguir incluyendo `{% csrf_token %}`. Las contraseñas de usuarios de prueba no deben subirse al repositorio en texto plano fuera de la documentación de demo (`README_DATOS_PRUEBA.md`). En un despliegue real, `SECRET_KEY` y credenciales de base de datos deberían moverse a un archivo `.env` que no se versiona; en local, conviene revisar que `.env` esté en `.gitignore`.

### Revisión de configuración sensible

En `discopro/settings.py` se mantiene `DEBUG=True` y `ALLOWED_HOSTS = ['*']`, lo cual es aceptable para desarrollo local pero **debe cambiarse antes de cualquier despliegue público**. La mantención de seguridad incluye documentar esta transición y revisar que `AUTH_PASSWORD_VALIDATORS` y `IsAuthenticated` en la API sigan activos.

### Auditoría periódica

Antes de cada entrega o demo importante, se recomienda recorrer el checklist de seguridad del documento de código: sesiones, CSRF, RBAC, IDOR, hashing, ORM. No se requieren herramientas especializadas; basta con revisión manual del código y prueba con usuarios de distintos roles.

---

## Mantención a cargo del coordinador de operaciones (usuario de negocio)

El coordinador de operaciones representa al lado funcional de Cruz Verde: despachadores, operadores de farmacia y motoristas. No modifica código, pero es clave para que la mantención tenga sentido de negocio.

### Validación funcional tras cambios

Cada vez que el desarrollador implementa una mejora o corrige un error, el coordinador —o quien simule ese rol en la evaluación— prueba el flujo completo con las credenciales de `README_DATOS_PRUEBA.md`: registrar un despacho como operador, revisarlo en el panel, entrar como motorista, iniciar ruta, marcar entregado o reportar incidencia. Esta validación confirma que la solución sigue resolviendo la problemática planteada.

### Reporte de incidencias y sugerencias

Los usuarios de prueba reportan al desarrollador cualquier comportamiento confuso o incorrecto: un botón que no responde, un estado de despacho que no cambia, un menú que no corresponde al rol. Esas observaciones alimentan la mantención correctiva y evolutiva.

### Priorización de mejoras

El coordinador indica qué funcionalidades aportan más valor: por ejemplo, notificaciones al motorista, reportes por farmacia o firma de entrega. El desarrollador usa esa priorización para planificar la mantención evolutiva sin desviarse del objetivo del negocio.

---

## Mantención a cargo del responsable de documentación

La documentación es parte de la vigencia del sistema. Si nadie entiende cómo instalar, probar o mantener Discopro, el software deja de ser usable aunque el código funcione.

### Documentos que deben mantenerse actualizados

El archivo `README.md` debe reflejar cómo instalar el proyecto, activar el entorno virtual, configurar la base de datos y ejecutar migraciones. `README_DATOS_PRUEBA.md` debe listar usuarios, contraseñas y flujos de demo vigentes. `DOCUMENTACION_SEGURIDAD_CODIGO.md` debe coincidir con las líneas reales del código cuando cambien vistas o permisos. Este plan de mantención (`PLAN_MANTENCION.md`) debe revisarse si el entorno deja de ser solo local y pasa a un servidor.

### Cuándo actualizar la documentación

Se actualiza la documentación cada vez que se agrega un rol, una pantalla, un endpoint de API o se cambian credenciales de prueba. También antes de cada presentación o entrega académica, para que la demo sea reproducible por cualquier evaluador con VS Code y MariaDB instalados.

---

## Mantención del entorno local (VS Code y máquina de desarrollo)

Como el sistema solo se corre en local desde VS Code, existe una capa de mantención sobre la propia máquina de desarrollo que no aplica a un servidor de producción pero sí al día a día del proyecto.

### Entorno virtual Python

El proyecto debe ejecutarse dentro de un entorno virtual (`venv`). Si se instalan paquetes nuevos, se actualiza `requirements.txt` con `pip freeze` para que otro integrante del equipo pueda replicar el entorno. Si el entorno se corrompe, se recrea el venv, se reinstalan dependencias y se verifica con `python manage.py runserver`.

### Base de datos local

MariaDB o MySQL debe estar en ejecución antes de levantar Django. Si la conexión falla, se revisan las variables en `.env` (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`). Tras cambios grandes en modelos, si hay dudas sobre el estado de la base, la opción más segura en desarrollo es borrar la base, recrearla, migrar y ejecutar de nuevo el seed.

### Servidor de desarrollo

En local se usa `python manage.py runserver`, no Gunicorn ni nginx. Eso implica que la mantención no incluye reiniciar servicios del sistema operativo ni configurar proxy reverso; basta con detener y volver a iniciar el servidor en la terminal de VS Code cuando se cambia código Python o settings. Los archivos estáticos se sirven en modo desarrollo según la configuración de Django; si se modifican CSS o templates, a veces es necesario refrescar el navegador con caché limpia.

### Control de versiones con Git

Todo cambio estable debe quedar registrado en Git con mensajes claros. Antes de una demo o entrega, conviene verificar que la rama principal tenga migraciones, seed y documentación al día. Git actúa como historial de mantención: permite volver a una versión anterior si un cambio introduce errores.

---

## Mantención evolutiva: hacia dónde puede crecer el sistema

Aunque hoy el proyecto corre solo en VS Code, el plan contempla cómo evolucionaría si Cruz Verde adoptara la solución de forma permanente.

En una primera etapa de evolución, se podrían agregar notificaciones al motorista cuando se le asigna un despacho, reportes más detallados por farmacia y permisos granulares en la API REST. En una segunda etapa, un portal accesible desde internet requeriría desplegar Django detrás de un servidor WSGI (como Gunicorn), un proxy (como nginx), HTTPS, `DEBUG=False` y `ALLOWED_HOSTS` restrictivo; esas configuraciones **no forman parte del entorno actual**, pero están identificadas para cuando el proyecto salga del ámbito académico o de demo local.

La escalabilidad, por ahora, se limita a mantener consultas eficientes e índices en base de datos. Si el número de despachos de prueba crece mucho, se puede paginar listados en el dashboard y en el portal del motorista. No se requieren métricas de CPU para decidir eso; basta con observar si las pantallas tardan en cargar durante la demo.

---

## Frecuencias recomendadas (adaptadas al entorno local)

Sin horarios ni turnos formales, estas frecuencias se entienden en función de **cuándo se trabaja en el proyecto**, no de un servidor 24/7.

**Antes de cada sesión de trabajo:** verificar que MariaDB esté activa, activar el entorno virtual y ejecutar `python manage.py runserver`.

**Antes de cada demo o entrega:** ejecutar `python manage.py check`, probar login con al menos tres roles, respaldar o regenerar datos con seed, revisar que la documentación coincida con el sistema.

**Cada vez que se modifica código:** probar el flujo afectado; si hay cambios en modelos, migrar y, si es necesario, respaldar la base.

**Periódicamente (cada pocas semanas de trabajo activo):** revisar dependencias en `requirements.txt`, recorrer checklist de seguridad, limpiar datos de prueba obsoletos.

**Antes de un posible despliegue futuro:** planificar por separado la mantención de servidor, respaldos automáticos, HTTPS y monitoreo; eso queda fuera del alcance operativo actual pero documentado como evolución.

---

## Herramientas disponibles hoy (sin infraestructura de producción)

El plan no asume Gunicorn, nginx, cron en servidor ni monitoreo de CPU. Las herramientas reales del proyecto son:

**Visual Studio Code** como entorno de edición y terminal integrada. **Python y venv** para dependencias aisladas. **Django** (`manage.py`) para migraciones, checks y servidor de desarrollo. **MariaDB/MySQL** en localhost, administrable con **HeidiSQL** si se prefiere interfaz gráfica. **Git** para versionado. **Archivos de log** en `logs/discopro.log`. **Scripts y documentación** del propio repositorio (`seed_arica_parinacota.py`, README, documentación de seguridad).

Si en el futuro se contrata hosting o un VPS, se sumarían herramientas de despliegue; por ahora, la mantención se centra en lo que el equipo controla en su máquina de desarrollo.

---

## Conclusión

Este plan de mantención es detallado y proactivo dentro del **marco real del proyecto**: una aplicación Django que se desarrolla y demuestra en VS Code, con base de datos local y usuarios de prueba documentados. Define **quién** mantiene cada aspecto (desarrollador, DBA, seguridad, operaciones, documentación), **qué** actividades corresponden a corrección, prevención y evolución, y **con qué medios** se ejecutan hoy, sin inventar métricas de servidor ni horarios que el equipo no tiene.

Así se asegura la vigencia de la solución en el tiempo: el código sigue funcionando, los datos de prueba son reproducibles, la seguridad está documentada y alineada con el código, y la documentación permite que cualquier persona retome el proyecto. Cuando Discopro deje de ser solo un entorno local, este plan servirá de base para ampliar la mantención hacia servidores, respaldos automáticos y despliegue continuo.

---

*Plan de mantención — Discopro Django / Cruz Verde — Entorno local VS Code*
