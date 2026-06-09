# Separación de Motos, Motoristas y Sucursales - Guía Completa

## Cambios Realizados

### 1. **Modelos Actualizados** (apps/motoristas/models.py)
- **Nuevo Modelo `Sucursal`**: Entidad independiente para gestionar sucursales
- **Nuevo Modelo `Moto`**: Entidad independiente para gestionar motos
- **Modelo `Motorista` Modificado**: 
  - Eliminados campos de vehículo (vehiculo_placa, marca_vehiculo, modelo_vehiculo, año_vehiculo)
  - Agregado campo `moto` (ForeignKey a Moto)
  - Agregado campo `sucursal` (ForeignKey a Sucursal)

### 2. **Formularios** (apps/motoristas/forms.py)
- `SucursalForm`: Crear/editar sucursales
- `MotoForm`: Crear/editar motos
- `MotoristaForm`: Editar motoristas (actualizado)
- `MotoristaCreateForm`: Crear nuevos motoristas (actualizado)

### 3. **Vistas** (apps/motoristas/views.py)
Se agregaron las siguientes vistas:

**Para Sucursales:**
- `lista_sucursales()`: Listar todas las sucursales
- `crear_sucursal()`: Crear nueva sucursal
- `editar_sucursal()`: Editar sucursal
- `eliminar_sucursal()`: Eliminar sucursal

**Para Motos:**
- `lista_motos()`: Listar todas las motos (con filtros por estado y sucursal)
- `crear_moto()`: Crear nueva moto
- `editar_moto()`: Editar moto
- `eliminar_moto()`: Eliminar moto

**Para Motoristas:**
- Actualizadas para usar los nuevos campos `moto` y `sucursal`

### 4. **URLs** (apps/motoristas/urls.py)
```
/motoristas/sucursales/                    - Listar sucursales
/motoristas/sucursales/crear/              - Crear sucursal
/motoristas/sucursales/<id>/editar/        - Editar sucursal
/motoristas/sucursales/<id>/eliminar/      - Eliminar sucursal

/motoristas/motos/                         - Listar motos
/motoristas/motos/crear/                   - Crear moto
/motoristas/motos/<id>/editar/             - Editar moto
/motoristas/motos/<id>/eliminar/           - Eliminar moto

/motoristas/                               - Listar motoristas
/motoristas/crear/                         - Crear motorista
/motoristas/<id>/editar/                   - Editar motorista
/motoristas/<id>/                          - Detalle motorista
```

### 5. **Templates Creados**
- `sucursales.html`: Listado de sucursales
- `sucursal_crear.html`: Formulario para crear sucursal
- `sucursal_editar.html`: Formulario para editar sucursal
- `sucursal_eliminar.html`: Confirmación de eliminación
- `motos.html`: Listado de motos
- `moto_crear.html`: Formulario para crear moto
- `moto_editar.html`: Formulario para editar moto
- `moto_eliminar.html`: Confirmación de eliminación

### 6. **Dashboard Actualizado**
Se agregó una sección "Acceso Rápido" con botones para:
- Gestionar Sucursales
- Gestionar Motos
- Gestionar Motoristas
- Ver Movimientos

## Cómo Usar

### Agregar una Sucursal
1. Desde el dashboard, haz clic en "Sucursales"
2. Haz clic en "Agregar Sucursal"
3. Completa el formulario con:
   - Nombre de la sucursal
   - Ciudad
   - Dirección
   - Teléfono (opcional)
   - Encargado (usuario responsable)
4. Guarda

### Agregar una Moto
1. Desde el dashboard, haz clic en "Motos"
2. Haz clic en "Agregar Moto"
3. Completa el formulario con:
   - Placa (única)
   - Marca
   - Modelo
   - Año
   - Color (opcional)
   - Sucursal (selecciona una sucursal)
   - Estado (Disponible, En Mantenimiento, Dañada, Retirada)
4. Guarda

### Agregar un Motorista
1. Desde el dashboard, haz clic en "Motoristas"
2. Haz clic en "Agregar Motorista"
3. Completa los datos del usuario y licencia
4. Asigna una moto (opcional)
5. Asigna una sucursal (requerido)
6. Guarda

### Filtrar Motos
En la página de motos, puedes filtrar por:
- **Estado**: Disponible, En Mantenimiento, Dañada, Retirada
- **Sucursal**: Selecciona una sucursal específica
- **Búsqueda**: Por placa, marca o modelo

### Filtrar Motoristas
En la página de motoristas, puedes filtrar por:
- **Estado**: Disponible, En Ruta, Inactivo, Bloqueado
- **Sucursal**: Selecciona una sucursal específica
- **Búsqueda**: Por nombre, RUT o placa de moto

## Base de Datos

Se creó la migración `0002_moto_remove_motorista_año_vehiculo_and_more.py` que:
- Crea tabla `moto` con campos: placa, marca, modelo, año, color, sucursal_id, estado, activo, creado_en, actualizado_en
- Crea tabla `sucursal_flota` (sucursal_flota para evitar conflicto con tabla existente) con campos: nombre, ciudad, direccion, telefono, encargado_id, activo, creado_en, actualizado_en
- Modifica tabla `motorista` eliminando los campos de vehículo y agregando moto_id y sucursal_id

## Notas Importantes

1. **Sucursal en Motorista**: Es obligatoria para todos los motoristas nuevos
2. **Moto en Motorista**: Es opcional, un motorista puede no tener moto asignada
3. **Eliminación de Sucursal**: Si una sucursal tiene motos, no se puede eliminar (hay protección PROTECT)
4. **Historial de datos**: Los motoristas existentes necesitan asignación de sucursal y moto

## Próximas Acciones Recomendadas

1. Asignar sucursales a todos los motoristas existentes
2. Crear registros de motos en el sistema
3. Asignar motos a motoristas
4. Verificar que los filtros en el dashboard funcionen correctamente con los nuevos datos
