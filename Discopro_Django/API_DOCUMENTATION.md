# Documentación de API REST - Discopro

## Base URL
```
http://localhost:8000/api/
```

## Autenticación
La API utiliza autenticación basada en sesión Django. Incluye el token CSRF en todas las peticiones POST, PUT, DELETE.

## Headers Requeridos
```
Content-Type: application/json
X-CSRFToken: [valor del token]
```

---

## Endpoints

### Departamentos

#### Listar Departamentos
```
GET /api/departamentos/
```

**Respuesta (200 OK):**
```json
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "codigo": "admin",
            "nombre": "Administrador"
        },
        {
            "id": 2,
            "codigo": "operador",
            "nombre": "Operador"
        }
    ]
}
```

#### Obtener Departamento
```
GET /api/departamentos/{id}/
```

#### Crear Departamento
```
POST /api/departamentos/
```

**Body:**
```json
{
    "codigo": "supervisor",
    "nombre": "Supervisor"
}
```

---

### Usuarios

#### Listar Usuarios
```
GET /api/usuarios/
```

#### Obtener Usuario
```
GET /api/usuarios/{id}/
```

#### Crear Usuario
```
POST /api/usuarios/
```

**Body:**
```json
{
    "username": "nuevouser",
    "email": "user@example.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "departamento": 1
}
```

#### Actualizar Usuario
```
PUT /api/usuarios/{id}/
PATCH /api/usuarios/{id}/
```

#### Eliminar Usuario
```
DELETE /api/usuarios/{id}/
```

---

### Motoristas

#### Listar Motoristas
```
GET /api/motoristas/
```

**Parámetros opcionales:**
- `search`: Buscar por nombre o licencia
- `estado`: Filtrar por estado (disponible, en_ruta, ocupado, inactivo)
- `ordering`: Ordenar por campo

**Respuesta:**
```json
{
    "count": 2,
    "results": [
        {
            "id": 1,
            "usuario": 3,
            "licencia": "LIC001",
            "vehiculo": "NQB-123",
            "estado": "disponible",
            "telefono": "3115555555",
            "ubicacion_actual": "4.7110,-74.0075",
            "fecha_registro": "2024-01-15"
        }
    ]
}
```

#### Obtener Motorista
```
GET /api/motoristas/{id}/
```

#### Crear Motorista
```
POST /api/motoristas/
```

**Body:**
```json
{
    "usuario": 3,
    "licencia": "LIC003",
    "vehiculo": "NQB-789",
    "estado": "disponible",
    "telefono": "3117777777",
    "ubicacion_actual": "4.7000,-74.0100"
}
```

#### Actualizar Motorista
```
PUT /api/motoristas/{id}/
PATCH /api/motoristas/{id}/
```

#### Actualizar Ubicación
```
PATCH /api/motoristas/{id}/actualizar_ubicacion/
```

**Body:**
```json
{
    "ubicacion_actual": "4.7150,-74.0050"
}
```

#### Cambiar Estado
```
PATCH /api/motoristas/{id}/cambiar_estado/
```

**Body:**
```json
{
    "estado": "en_ruta"
}
```

#### Eliminar Motorista
```
DELETE /api/motoristas/{id}/
```

---

### Sucursales

#### Listar Sucursales
```
GET /api/sucursales/
```

**Respuesta:**
```json
{
    "count": 3,
    "results": [
        {
            "id": 1,
            "nombre": "Sucursal Centro",
            "direccion": "Calle Principal 123",
            "ciudad": "Bogotá",
            "telefono": "3101234567",
            "email": "centro@discopro.com"
        }
    ]
}
```

#### Obtener Sucursal
```
GET /api/sucursales/{id}/
```

#### Crear Sucursal
```
POST /api/sucursales/
```

**Body:**
```json
{
    "nombre": "Sucursal Este",
    "direccion": "Avenida Circunvalar 100",
    "ciudad": "Bogotá",
    "telefono": "3104444444",
    "email": "este@discopro.com"
}
```

#### Actualizar Sucursal
```
PUT /api/sucursales/{id}/
PATCH /api/sucursales/{id}/
```

#### Eliminar Sucursal
```
DELETE /api/sucursales/{id}/
```

---

### Movimientos

#### Listar Movimientos
```
GET /api/movimientos/
```

**Parámetros opcionales:**
- `estado`: Filtrar por estado (pendiente, en_progreso, completado, cancelado)
- `tipo`: Filtrar por tipo (entrega, retiro)
- `motorista`: Filtrar por ID de motorista
- `fecha_desde`: Filtrar desde fecha
- `fecha_hasta`: Filtrar hasta fecha

**Respuesta:**
```json
{
    "count": 5,
    "results": [
        {
            "id": 1,
            "despacho_numero": "DSP001",
            "motorista": 1,
            "sucursal": 1,
            "tipo": "entrega",
            "estado": "completado",
            "observaciones": "Entrega realizada",
            "fecha_creacion": "2024-01-15T10:30:00Z",
            "fecha_actualizacion": "2024-01-15T12:00:00Z",
            "fecha_entrega": "2024-01-15T12:00:00Z"
        }
    ]
}
```

#### Obtener Movimiento
```
GET /api/movimientos/{id}/
```

#### Crear Movimiento
```
POST /api/movimientos/
```

**Body:**
```json
{
    "despacho_numero": "DSP010",
    "motorista": 1,
    "sucursal": 1,
    "tipo": "entrega",
    "observaciones": "Cliente requiere firma"
}
```

#### Actualizar Movimiento
```
PUT /api/movimientos/{id}/
PATCH /api/movimientos/{id}/
```

#### Actualizar Estado
```
PATCH /api/movimientos/{id}/actualizar_estado/
```

**Body:**
```json
{
    "estado": "en_progreso",
    "observaciones": "Motorista en camino"
}
```

#### Marcar como Completado
```
PATCH /api/movimientos/{id}/completar/
```

**Body:**
```json
{
    "observaciones": "Entrega completada sin novedad"
}
```

#### Eliminar Movimiento
```
DELETE /api/movimientos/{id}/
```

---

### Reportes

#### Listar Reportes
```
GET /api/reportes/
```

**Parámetros opcionales:**
- `tipo`: Filtrar por tipo (movimientos, motoristas, general)
- `fecha_desde`: Filtrar desde fecha
- `fecha_hasta`: Filtrar hasta fecha

#### Obtener Reporte
```
GET /api/reportes/{id}/
```

#### Crear Reporte
```
POST /api/reportes/
```

**Body:**
```json
{
    "titulo": "Reporte de Entregas - Enero 2024",
    "tipo": "movimientos",
    "periodo_desde": "2024-01-01",
    "periodo_hasta": "2024-01-31"
}
```

#### Eliminar Reporte
```
DELETE /api/reportes/{id}/
```

---

## Códigos de Estado HTTP

| Código | Significado |
|--------|------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado |
| 204 | No Content - Solicitud exitosa sin contenido |
| 400 | Bad Request - Solicitud inválida |
| 401 | Unauthorized - No autenticado |
| 403 | Forbidden - No permitido |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

---

## Filtrado y Búsqueda

### Búsqueda
```
GET /api/motoristas/?search=juan
```

### Filtrado
```
GET /api/movimientos/?estado=completado&tipo=entrega
```

### Ordenamiento
```
GET /api/motoristas/?ordering=-fecha_registro
```

Prefija con `-` para orden descendente.

---

## Paginación

La API retorna 10 resultados por página por defecto.

```
GET /api/motoristas/?page=2
```

---

## Ejemplo de Solicitud Completa con cURL

```bash
# Login primero
curl -X POST http://localhost:8000/login/ \
  -d "username=testuser&password=testpass123" \
  -c cookies.txt

# Obtener CSRF token (desde respuesta HTML o el header)

# Crear motorista
curl -X POST http://localhost:8000/api/motoristas/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: [token]" \
  -b cookies.txt \
  -d '{
    "usuario": 3,
    "licencia": "LIC999",
    "vehiculo": "NQB-999",
    "estado": "disponible",
    "telefono": "3119999999"
  }'
```

---

## Ejemplo de Solicitud con JavaScript

```javascript
// Obtener CSRF token
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Crear motorista
fetch('/api/motoristas/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
        usuario: 3,
        licencia: 'LIC999',
        vehiculo: 'NQB-999',
        estado: 'disponible',
        telefono: '3119999999'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Errores Comunes

### Error 401 - Unauthorized
Asegúrate de estar autenticado. Visita `/login/` primero.

### Error 403 - CSRF token missing
Incluye el header `X-CSRFToken` en solicitudes POST/PUT/DELETE.

### Error 400 - Validation Error
Verifica que los datos cumplan con los requisitos del modelo (campos requeridos, formatos válidos, etc.)

### Error 404 - Not Found
Verifica que la URL y el ID del recurso sean correctos.

---

## Rate Limiting

Actualmente no hay límite de tasa, pero se recomienda:
- Máximo 100 solicitudes por minuto
- Máximo 1000 solicitudes por hora

---

## CORS

Para solicitudes desde diferente dominio, asegúrate que:
1. Tu frontend está en `ALLOWED_HOSTS`
2. CORS está habilitado en `settings.py`
3. El header `Access-Control-Allow-Origin` es configurado

---

**Última actualización:** 2024
**Versión de API:** v1.0
