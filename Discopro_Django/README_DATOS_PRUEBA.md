# Datos de Prueba - Discopro Logística (Arica / Parinacota)

Este archivo documenta los datos insertados con:

```bash
python seed_arica_parinacota.py
```

Los datos son referenciales para pruebas locales. Las farmacias son puntos de origen (sin acceso al sistema).

## Usuarios de Prueba

| Rol | Usuario | Contraseña | Qué puede probar |
| --- | --- | --- | --- |
| Administrador | `admin_arica` | `AdminArica123` | Acceso total, administración de usuarios, farmacias, motos, motoristas y movimientos |
| Supervisor / Gerencia | `despacho_arica` | `DespachoArica123` | Gestión de farmacias, motos, motoristas y movimientos |
| Operadora | `operador_arica` | `OperadorArica123` | Registrar movimientos/despachos y descargar Excel |
| Motorista | `motorista_vega` | `Motorista123` | Portal del motorista |
| Motorista | `motorista_rojas` | `Motorista123` | Portal del motorista |
| Motorista | `motorista_condori` | `Motorista123` | Portal del motorista |
| Motorista | `motorista_mamani` | `Motorista123` | Portal del motorista |

## Farmacias de origen cargadas

- Cruz Verde Arica Centro
- Cruz Verde Mall Plaza Arica
- Cruz Verde Santa María Arica
- Cruz Verde Putre Referencial

Todas quedan con región **Arica** o **Parinacota** (regiones independientes), no combinadas.

## Motos cargadas

- `CV-AR-101` Honda XR 150L
- `CV-AR-102` Yamaha FZ 150
- `CV-AR-103` Suzuki GN 125
- `CV-AR-104` Honda CB 125F
- `CV-AR-105` Bajaj Boxer 150

## Asignaciones operativas

Las motos y farmacias se asignan mediante la tabla `AsignacionOperativa`:

- Carlos Vega → `CV-AR-101` → Cruz Verde Arica Centro
- Paula Rojas → `CV-AR-102` → Cruz Verde Mall Plaza Arica
- Luis Condori → `CV-AR-103` → Cruz Verde Santa María Arica
- Elena Mamani → `CV-AR-104` → Cruz Verde Putre Referencial

## Flujo recomendado de prueba

1. Entrar con `admin_arica` y revisar **Administración de usuarios** (`/usuarios/administracion/`).
2. Entrar con `despacho_arica` (supervisor) y revisar Farmacias, Motos y Motoristas.
3. Entrar con `operador_arica` y registrar un movimiento: al elegir farmacia de origen solo verá motoristas de esa farmacia.
4. Descargar el Excel de movimientos.
5. Entrar con un motorista (p. ej. `motorista_vega`) y usar el portal: despachos, iniciar ruta, entregado, incidencias.

## Despachos de prueba

- `COD-1001` → `motorista_vega` → Pendiente
- `COD-1002` → `motorista_vega` → En ruta
- `COD-1003` → `motorista_rojas` → Pendiente
- `COD-1004` → `motorista_rojas` → Incidencia
- `COD-1005` → `motorista_condori` → Pendiente
- `COD-1006` → `motorista_mamani` → Pendiente
