# Documento de Resultados y Evidencias de Pruebas de Software

**Proyecto:** LogiPro — Plataforma logística web para Discopro Ltda.  
**Framework:** Django `unittest` (`django.test.TestCase`, `Client`)  
**Archivo de pruebas:** `tests.py` (32 casos, alineados al sistema vigente)  
**Ejecución de referencia:** `py manage.py test --verbosity=2`  
**Fecha del reporte:** 4 de julio de 2026  
**Versión analizada:** Django 6.0.5 · migraciones hasta `motoristas.0007`, `movimientos.0007`, `usuarios.0003`  
**Estado del proyecto:** **Operativo — suite de pruebas verde al 100 %**

---

## 1. DASHBOARD EJECUTIVO — RESUMEN DE PRUEBAS

```
╔══════════════════════════════════════════════════════════════════╗
║  LOGIPRO — RESUMEN EJECUTIVO DE PRUEBAS UNITARIAS               ║
╠══════════════════════════════════════════════════════════════════╣
║  Fecha de ejecución .............. 04/07/2026                    ║
║  Entorno ......................... Django 6.0.5 / Python 3.14    ║
║  Base de datos de prueba ......... MariaDB (test_discopro_db)    ║
║  Total de tests .................. 32                             ║
║  Tests aprobados ................. 32                             ║
║  Tests fallidos .................. 0                              ║
║  Tests con error ................. 0                              ║
║  Tasa de éxito (Pass Rate) ....... 100,0 %                       ║
║  Tiempo total de suite ........... 40,366 s                      ║
║  Tiempo promedio por test ........ ~1,26 s                       ║
╚══════════════════════════════════════════════════════════════════╝
```

| Métrica | Valor |
|---------|------:|
| Total de Tests | 32 |
| Tests Aprobados | 32 |
| Tests Fallidos | 0 |
| Tests con Error | 0 |
| **Tasa de Éxito (Pass Rate)** | **100,0 %** |
| Tiempo Total | 40,366 s |
| Tiempo Promedio por Test | 1,26 s |

### Interpretación ejecutiva

La suite fue **reescrita por completo** para reflejar la arquitectura actual de LogiPro: separación de credenciales, asignaciones operativas, farmacia de origen, geografía chilena (Arica / Parinacota independientes), validación motorista ↔ farmacia, portal del motorista y matriz de permisos por rol.

Durante la ejecución se detectó y corrigió una **deuda de migración** (`vehiculo_placa` legacy en BD sin campo en modelo); se aplicó `motoristas.0007_remove_legacy_motorista_fields` antes de obtener resultados definitivos.

---

## 2. COBERTURA DE REQUERIMIENTOS

Los requerimientos evaluados corresponden al **sistema LogiPro implementado**, no a una especificación externa desactualizada.

| ID | Requerimiento del sistema actual | Estado implementación | Tests que lo cubren | Cobertura |
|----|----------------------------------|----------------------|---------------------|----------:|
| **RQ-AUTH-01** | Login con usuario y contraseña (Django Auth) | Completamente implementado | 4 tests `AutenticacionTest` | **100 %** |
| **RQ-AUTH-02** | Redirección por rol post-login (operador → dashboard, motorista → portal) | Completamente implementado | `test_login_correcto_operador`, `test_redireccion_motorista_al_portal` | **100 %** |
| **RQ-ROL-01** | Roles: administrador, supervisor, operador, motorista | Completamente implementado | `UsuarioModelTest`, `PermisosAccesoTest` | **100 %** |
| **RQ-ROL-02** | Permisos: flota (admin/supervisor), usuarios (solo admin) | Completamente implementado | 4 tests `PermisosAccesoTest` | **100 %** |
| **RQ-FARM-01** | Farmacias origen con región, provincia, comuna | Completamente implementado | `FarmaciaModelTest` | **100 %** |
| **RQ-GEO-01** | Regiones Arica y Parinacota como entidades separadas | Completamente implementado | `test_regiones_arica_y_parinacota_separadas`, `test_cascada_geografica_putre` | **100 %** |
| **RQ-ASIG-01** | Asignación moto + farmacia vía `AsignacionOperativa` | Completamente implementado | 3 tests `MotoristaAsignacionTest` | **100 %** |
| **RQ-MOV-01** | Registro de despacho con farmacia origen y dirección autocompletada | Completamente implementado | `MovimientoModelTest`, `DashboardIntegracionTest` | **100 %** |
| **RQ-MOV-02** | Unicidad global de `numero_despacho` | Completamente implementado | `test_numero_despacho_unico_global` | **100 %** |
| **RQ-MOV-03** | Motorista solo opera despachos de su farmacia asignada | Completamente implementado | `ValidacionAsignacionTest`, `DashboardIntegracionTest` | **100 %** |
| **RQ-API-01** | API dirección y motoristas filtrados por farmacia | Completamente implementado | 2 tests `ApiFarmaciaTest` | **100 %** |
| **RQ-PORT-01** | Portal motorista: iniciar ruta, marcar entregado | Completamente implementado | 3 tests `PortalMotoristaTest` | **100 %** |
| **RQ-PORT-02** | Portal exclusivo para rol motorista | Completamente implementado | `test_operador_no_accede_portal` | **100 %** |
| **RQ-DASH-01** | Filtro de movimientos por dirección origen/destino | Completamente implementado | `test_filtro_movimientos_por_direccion` | **100 %** |

### Resumen porcentual global

| Categoría | Completamente | Parcialmente | No implementado |
|-----------|:-------------:|:------------:|:---------------:|
| Requerimientos LogiPro evaluados (14) | **100 %** | 0 % | 0 % |
| Cobertura automatizada en `tests.py` | **14 / 14** | — | — |

### Funcionalidades del sistema sin test automatizado aún

| Funcionalidad | Observación |
|---------------|-------------|
| Exportación Excel de movimientos | Existe en `movimientos/views.py`; sin test |
| CRUD completo farmacias/motos vía formularios | Cubierto indirectamente por permisos; sin test de formulario |
| Módulo de reportes | Sin tests en suite actual |
| API REST DRF (`/api/`) | Sin tests en suite actual |
| Geografía JS en cascada (frontend) | Validada en backend (`geografia.py`); sin test Selenium |

---

## 3. DESGLOSE VISUAL DE TESTS (Por Módulo)

### Módulo: Autenticación (`AutenticacionTest`) — 4/4

| Test | Resultado |
|------|-----------|
| `test_login_page_accesible` | :white_check_mark: PASS |
| `test_login_correcto_operador` | :white_check_mark: PASS |
| `test_login_incorrecto_rechazado` | :white_check_mark: PASS |
| `test_redireccion_motorista_al_portal` | :white_check_mark: PASS |

### Módulo: Usuarios y roles (`UsuarioModelTest`) — 3/3

| Test | Resultado |
|------|-----------|
| `test_crear_usuario_perfil` | :white_check_mark: PASS |
| `test_usuario_string_muestra_rol` | :white_check_mark: PASS |
| `test_permisos_por_rol` | :white_check_mark: PASS |

### Módulo: Farmacias y geografía (`FarmaciaModelTest`) — 3/3

| Test | Resultado |
|------|-----------|
| `test_crear_farmacia_con_geografia` | :white_check_mark: PASS |
| `test_regiones_arica_y_parinacota_separadas` | :white_check_mark: PASS |
| `test_cascada_geografica_putre` | :white_check_mark: PASS |

### Módulo: Motoristas y asignaciones (`MotoristaAsignacionTest`) — 3/3

| Test | Resultado |
|------|-----------|
| `test_crear_motorista_con_asignacion` | :white_check_mark: PASS |
| `test_licencia_unica` | :white_check_mark: PASS |
| `test_sincronizar_asignacion_desactiva_anterior` | :white_check_mark: PASS |

### Módulo: Movimientos (`MovimientoModelTest`) — 3/3

| Test | Resultado |
|------|-----------|
| `test_crear_movimiento_estado_pendiente` | :white_check_mark: PASS |
| `test_direccion_origen_autocompletada` | :white_check_mark: PASS |
| `test_numero_despacho_unico_global` | :white_check_mark: PASS |

### Módulo: Validación motorista ↔ farmacia (`ValidacionAsignacionTest`) — 4/4

| Test | Resultado |
|------|-----------|
| `test_motorista_pertenece_a_su_farmacia` | :white_check_mark: PASS |
| `test_motorista_no_pertenece_a_otra_farmacia` | :white_check_mark: PASS |
| `test_validar_asignacion_retorna_error_cruzado` | :white_check_mark: PASS |
| `test_validar_asignacion_ok_misma_farmacia` | :white_check_mark: PASS |

### Módulo: Dashboard — integración (`DashboardIntegracionTest`) — 3/3

| Test | Resultado |
|------|-----------|
| `test_registrar_despacho_valido` | :white_check_mark: PASS |
| `test_rechaza_motorista_de_otra_farmacia` | :white_check_mark: PASS |
| `test_filtro_movimientos_por_direccion` | :white_check_mark: PASS |

### Módulo: API farmacia (`ApiFarmaciaTest`) — 2/2

| Test | Resultado |
|------|-----------|
| `test_api_direccion_farmacia` | :white_check_mark: PASS |
| `test_api_motoristas_por_farmacia` | :white_check_mark: PASS |

### Módulo: Portal motorista (`PortalMotoristaTest`) — 3/3

| Test | Resultado |
|------|-----------|
| `test_iniciar_ruta_cambia_estado` | :white_check_mark: PASS |
| `test_marcar_entregado` | :white_check_mark: PASS |
| `test_operador_no_accede_portal` | :white_check_mark: PASS |

### Módulo: Permisos de acceso (`PermisosAccesoTest`) — 4/4

| Test | Resultado |
|------|-----------|
| `test_operador_no_accede_lista_farmacias` | :white_check_mark: PASS |
| `test_supervisor_accede_lista_farmacias` | :white_check_mark: PASS |
| `test_operador_no_accede_admin_usuarios` | :white_check_mark: PASS |
| `test_administrador_accede_admin_usuarios` | :white_check_mark: PASS |

---

## 4. MATRIZ DE TRAZABILIDAD (Casos de Prueba vs Resultados)

| ID Caso | Descripción | Requerimiento | Estado | Test unitario | Observaciones |
|---------|-------------|---------------|--------|---------------|---------------|
| CP-001 | Página login accesible (HTTP 200, branding LogiPro) | RQ-AUTH-01 | :white_check_mark: | `AutenticacionTest.test_login_page_accesible` | — |
| CP-002 | Login exitoso operador → dashboard | RQ-AUTH-01 / RQ-AUTH-02 | :white_check_mark: | `test_login_correcto_operador` | Usa `username`, no RUT |
| CP-003 | Login fallido no autentica sesión | RQ-AUTH-01 | :white_check_mark: | `test_login_incorrecto_rechazado` | — |
| CP-004 | Motorista redirigido al portal | RQ-AUTH-02 | :white_check_mark: | `test_redireccion_motorista_al_portal` | URL `/portal-motorista/` |
| CP-005 | Crear perfil Usuario con RUT y rol | RQ-ROL-01 | :white_check_mark: | `UsuarioModelTest.test_crear_usuario_perfil` | RUT en perfil, no en login |
| CP-006 | `__str__` de Usuario muestra rol legible | RQ-ROL-01 | :white_check_mark: | `test_usuario_string_muestra_rol` | Ej: `(Operadora)` |
| CP-007 | Matriz permisos admin / supervisor / operador | RQ-ROL-02 | :white_check_mark: | `test_permisos_por_rol` | Funciones en `permissions.py` |
| CP-008 | Farmacia con geografía chilena | RQ-FARM-01 | :white_check_mark: | `FarmaciaModelTest.test_crear_farmacia_con_geografia` | — |
| CP-009 | Regiones Arica y Parinacota separadas | RQ-GEO-01 | :white_check_mark: | `test_regiones_arica_y_parinacota_separadas` | No existe región compuesta |
| CP-010 | Cascada geográfica Putre (Parinacota) | RQ-GEO-01 | :white_check_mark: | `test_cascada_geografica_putre` | Backend `geografia.py` |
| CP-011 | Motorista con moto y farmacia asignadas | RQ-ASIG-01 | :white_check_mark: | `MotoristaAsignacionTest.test_crear_motorista_con_asignacion` | Propiedades `moto_actual`, `sucursal_actual` |
| CP-012 | Licencia de conducir única en BD | RQ-ASIG-01 | :white_check_mark: | `test_licencia_unica` | `IntegrityError` |
| CP-013 | Nueva asignación desactiva la anterior | RQ-ASIG-01 | :white_check_mark: | `test_sincronizar_asignacion_desactiva_anterior` | `sincronizar_asignacion()` |
| CP-014 | Movimiento creado en estado pendiente | RQ-MOV-01 | :white_check_mark: | `MovimientoModelTest.test_crear_movimiento_estado_pendiente` | — |
| CP-015 | Dirección origen autocompletada desde farmacia | RQ-MOV-01 | :white_check_mark: | `test_direccion_origen_autocompletada` | Hook en `Movimiento.save()` |
| CP-016 | Número de despacho único (global) | RQ-MOV-02 | :white_check_mark: | `test_numero_despacho_unico_global` | Constraint BD |
| CP-017 | Motorista pertenece solo a su farmacia | RQ-MOV-03 | :white_check_mark: | `ValidacionAsignacionTest` (4 tests) | — |
| CP-018 | POST dashboard registra despacho válido | RQ-MOV-01 | :white_check_mark: | `DashboardIntegracionTest.test_registrar_despacho_valido` | Integración HTTP |
| CP-019 | POST dashboard rechaza motorista de otra farmacia | RQ-MOV-03 | :white_check_mark: | `test_rechaza_motorista_de_otra_farmacia` | Sin insert en BD |
| CP-020 | Filtro por dirección origen/destino | RQ-DASH-01 | :white_check_mark: | `test_filtro_movimientos_por_direccion` | `filtrar_movimientos()` |
| CP-021 | API JSON dirección de farmacia | RQ-API-01 | :white_check_mark: | `ApiFarmaciaTest.test_api_direccion_farmacia` | `/farmacia/api/<id>/direccion/` |
| CP-022 | API JSON motoristas por farmacia | RQ-API-01 | :white_check_mark: | `test_api_motoristas_por_farmacia` | Usado por `farmacia-origen.js` |
| CP-023 | Iniciar ruta → estado `en_ruta` | RQ-PORT-01 | :white_check_mark: | `PortalMotoristaTest.test_iniciar_ruta_cambia_estado` | — |
| CP-024 | Marcar entregado → estado `entregado` + timestamp | RQ-PORT-01 | :white_check_mark: | `test_marcar_entregado` | Campo `entregado_en` |
| CP-025 | Operador bloqueado del portal motorista | RQ-PORT-02 | :white_check_mark: | `test_operador_no_accede_portal` | Redirect a dashboard |
| CP-026 | Operador no accede CRUD farmacias | RQ-ROL-02 | :white_check_mark: | `PermisosAccesoTest.test_operador_no_accede_lista_farmacias` | — |
| CP-027 | Supervisor accede CRUD farmacias | RQ-ROL-02 | :white_check_mark: | `test_supervisor_accede_lista_farmacias` | — |
| CP-028 | Operador no accede admin usuarios | RQ-ROL-02 | :white_check_mark: | `test_operador_no_accede_admin_usuarios` | — |
| CP-029 | Administrador accede admin usuarios | RQ-ROL-02 | :white_check_mark: | `test_administrador_accede_admin_usuarios` | `/usuarios/administracion/` |

---

## 5. MATRIZ DE CONTRASTE Y ANÁLISIS DE DISCREPANCIAS

No se detectaron fallos en la suite actual. Los hallazgos siguientes son **brechas entre el producto LogiPro y requerimientos históricos no incluidos en el alcance actual**, o **áreas sin automatización**.

| ID | Resultado esperado (referencia histórica) | Resultado en LogiPro actual | Severidad | Causa raíz / observación |
|----|-------------------------------------------|----------------------------|-----------|--------------------------|
| REF-01 | Login con RUT como credencial | Login con `username` Django | **Informativa** | Diseño actual separa RUT (perfil) de credencial (`auth.User.username`). No es defecto de la suite; es decisión de arquitectura. |
| REF-02 | Bloqueo tras 3 intentos fallidos | Intentos ilimitados | **Media** | Fuera del alcance implementado; no hay contador en `login_view`. |
| REF-03 | Folio numérico 8–10 dígitos (Cruz Verde) | `numero_despacho` alfanumérico libre | **Informativa** | LogiPro usa códigos tipo `COD-1001` / `REG-001`; regla distinta al legado RF50. |
| REF-04 | Duplicidad de folio solo el mismo día | Unicidad permanente | **Baja** | Implementado y probado (`test_numero_despacho_unico_global`); semántica distinta. |
| REF-05 | Filtro PII Ley 19.628 en observaciones | Sin filtro en `comentario_incidencia` | **Media** | No implementado; sin test. |
| REF-06 | Locking concurrente en edición de folios | Edición directa sin bloqueo | **Media** | No implementado; sin test. |
| REF-07 | Columnas legacy `vehiculo_placa` en BD | Eliminadas en migración 0007 | **Resuelta** | Causaba ERROR en tests; corregido con `0007_remove_legacy_motorista_fields`. |

---

## Anexo A — Evidencia de ejecución

```text
Found 32 test(s).
System check identified 1 issue (0 silenced).
................................
----------------------------------------------------------------------
Ran 32 tests in 40.366s

OK
```

## Anexo B — Comandos de reproducción

```powershell
cd Discopro_Django
py manage.py migrate
py manage.py test --verbosity=2
```

## Anexo C — Estructura de la suite (`tests.py`)

| Clase | Tests | Enfoque |
|-------|------:|---------|
| `AutenticacionTest` | 4 | Login, sesión, redirección por rol |
| `UsuarioModelTest` | 3 | Modelo, roles, permisos |
| `FarmaciaModelTest` | 3 | Geografía, regiones |
| `MotoristaAsignacionTest` | 3 | Asignaciones operativas |
| `MovimientoModelTest` | 3 | Modelo, autocompletado origen |
| `ValidacionAsignacionTest` | 4 | Regla motorista ↔ farmacia |
| `DashboardIntegracionTest` | 3 | POST HTTP, filtros |
| `ApiFarmaciaTest` | 2 | Endpoints JSON |
| `PortalMotoristaTest` | 3 | Flujo estados portal |
| `PermisosAccesoTest` | 4 | Control acceso por rol |

## Anexo D — Documentación complementaria

| Documento | Contenido |
|-----------|-----------|
| `DOCUMENTACION_SISTEMA_FUNCIONAL_LOGIPRO.md` | Arquitectura, BD, URLs, código de referencia |
| `README_DATOS_PRUEBA.md` | Usuarios y datos seed Arica/Parinacota |

---

*Reporte generado tras actualización de `tests.py`, migración `motoristas.0007` y ejecución exitosa de la suite completa sobre el sistema LogiPro vigente.*
