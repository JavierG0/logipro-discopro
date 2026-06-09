-- --------------------------------------------------------
-- SCRIPT DE INSERCIÓN PARA DISCOPRO (MARIADB / HEIDISQL)
-- --------------------------------------------------------

-- 1. Opcional: Desactivar temporalmente revisión de llaves foráneas 
--    y limpiar tablas si deseas empezar desde cero. 
--    (Descomenta las siguientes líneas si quieres borrar datos existentes).
-- SET FOREIGN_KEY_CHECKS=0;
-- TRUNCATE TABLE usuario;
-- TRUNCATE TABLE departamento;
-- TRUNCATE TABLE auth_user;
-- SET FOREIGN_KEY_CHECKS=1;


-- 2. Insertar Departamentos
INSERT INTO departamento (id, nombre, tipo, descripcion, creado_en, actualizado_en) VALUES 
(1, 'Administración Central', 'admin', 'Departamento de administración del sistema', NOW(), NOW()),
(2, 'Despacho General', 'despacho', 'Departamento de despachos y asignaciones', NOW(), NOW()),
(3, 'Operaciones', 'operacion', 'Operaciones generales y motoristas', NOW(), NOW())
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);


-- 3. Insertar Usuarios base en la tabla nativa de Django (auth_user)
-- Las contraseñas están hasheadas según el formato pbkdf2_sha256 de Django.
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
(1, 'pbkdf2_sha256$1200000$wfj5vyNFN9mng3WBEGXXFf$2ME6RTzY1n29SsS4r2LANFE2HQ+0mCziZt4oiQtAlX0=', NULL, 1, 'admin', 'Super', 'Administrador', 'admin@discopro.com', 1, 1, NOW()),
(2, 'pbkdf2_sha256$1200000$CKwod0HbC3Y8U0pR1aFOF6$GZdTqoF76ETZa5lGyxDVn/ITc/4isUdW8mrvuaE3t8Q=', NULL, 0, 'despacho1', 'Juan', 'Despachador', 'despacho1@discopro.com', 1, 1, NOW()),
(3, 'pbkdf2_sha256$1200000$CKwod0HbC3Y8U0pR1aFOF6$GZdTqoF76ETZa5lGyxDVn/ITc/4isUdW8mrvuaE3t8Q=', NULL, 0, 'motorista1', 'Carlos', 'Piloto', 'motorista1@discopro.com', 0, 1, NOW()),
(4, 'pbkdf2_sha256$1200000$CKwod0HbC3Y8U0pR1aFOF6$GZdTqoF76ETZa5lGyxDVn/ITc/4isUdW8mrvuaE3t8Q=', NULL, 0, 'motorista2', 'Ana', 'Ruta', 'motorista2@discopro.com', 0, 1, NOW())
ON DUPLICATE KEY UPDATE username=VALUES(username);


-- 4. Insertar Perfiles en tu tabla personalizada 'usuario'
-- Estos perfiles están vinculados por foreign keys a los auth_user y departamentos creados arriba.
INSERT INTO usuario (rut, telefono, rol, estado, foto_perfil, ultimo_login, creado_en, actualizado_en, departamento_id, user_id) VALUES
('11111111-1', '+56911111111', 'administrador', 1, '', NULL, NOW(), NOW(), 1, 1),
('22222222-2', '+56922222222', 'despachador', 1, '', NULL, NOW(), NOW(), 2, 2),
('33333333-3', '+56933333333', 'motorista', 1, '', NULL, NOW(), NOW(), 3, 3),
('44444444-4', '+56944444444', 'motorista', 1, '', NULL, NOW(), NOW(), 3, 4)
ON DUPLICATE KEY UPDATE rut=VALUES(rut);

COMMIT;