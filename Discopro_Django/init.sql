-- Script de inicialización para MariaDB en Docker

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS discopro_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Seleccionar la base de datos
USE discopro_db;

-- Crear tabla de departamentos
CREATE TABLE IF NOT EXISTS usuarios_departamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insertar departamentos iniciales
INSERT IGNORE INTO usuarios_departamento (codigo, nombre) VALUES
    ('admin', 'Administrador'),
    ('operador', 'Operador'),
    ('motorista', 'Motorista'),
    ('supervisor', 'Supervisor');

-- Crear tabla de sucursales
CREATE TABLE IF NOT EXISTS movimientos_sucursal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    direccion VARCHAR(255),
    ciudad VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear tabla de logs
CREATE TABLE IF NOT EXISTS audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100),
    model VARCHAR(100),
    object_id INT,
    change_message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (user_id),
    INDEX (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Crear índices útiles
CREATE INDEX idx_email ON auth_user(email);
CREATE INDEX idx_username ON auth_user(username);

-- Mensajes de éxito
SELECT 'Base de datos Discopro inicializada correctamente' AS mensaje;
