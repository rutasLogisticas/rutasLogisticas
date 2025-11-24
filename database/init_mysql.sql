-- Script completo de inicialización de la base de datos
-- Este script crea todas las tablas necesarias y datos iniciales

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS rutas_logisticas 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE rutas_logisticas;

-- =====================================================
-- TABLAS DE ROLES Y PERMISOS
-- =====================================================

-- Crear tabla de roles
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX idx_roles_name (name)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear tabla de permisos
CREATE TABLE IF NOT EXISTS permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    resource VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX idx_permissions_name (name),
    INDEX idx_permissions_resource (resource),
    INDEX idx_permissions_action (action)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear tabla intermedia role_permissions
CREATE TABLE IF NOT EXISTS role_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (permission_id) REFERENCES permissions(id),
    INDEX idx_role_permissions_role_id (role_id),
    INDEX idx_role_permissions_permission_id (permission_id)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- =====================================================
-- TABLA DE USUARIOS (CON ROLE_ID)
-- =====================================================

-- Crear tabla de usuarios con role_id
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    security_question1 VARCHAR(255),
    security_answer1_hash VARCHAR(255),
    security_question2 VARCHAR(255),
    security_answer2_hash VARCHAR(255),
    FOREIGN KEY (role_id) REFERENCES roles(id),
    INDEX idx_users_role_id (role_id)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- =====================================================
-- OTRAS TABLAS DEL SISTEMA
-- =====================================================

-- Tabla de vehículos
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    vehicle_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'disponible',
    is_available BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabla de conductores
CREATE TABLE IF NOT EXISTS drivers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    document_number VARCHAR(20) UNIQUE NOT NULL,
    license_type VARCHAR(10) NOT NULL,
    status VARCHAR(20) DEFAULT 'disponible',
    is_available BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    company VARCHAR(200),
    client_type VARCHAR(20) DEFAULT 'individual',
    status VARCHAR(20) DEFAULT 'activo',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabla de pedidos
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    client_id INT NOT NULL,
    driver_id INT NULL,
    vehicle_id INT NULL,
    origin_address VARCHAR(300) NOT NULL,
    destination_address VARCHAR(300) NOT NULL,
    origin_city VARCHAR(100) NOT NULL,
    destination_city VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    weight DECIMAL(10,2) NULL,
    volume DECIMAL(10,2) NULL,
    value DECIMAL(10,2) NULL,
    status VARCHAR(20) DEFAULT 'pendiente' NOT NULL,
    priority VARCHAR(20) DEFAULT 'media' NOT NULL,
    delivery_date DATETIME NULL,
    delivered_date DATETIME NULL,
    notes TEXT NULL,
    tracking_code VARCHAR(50) UNIQUE NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_client_id (client_id),
    INDEX idx_driver_id (driver_id),
    INDEX idx_vehicle_id (vehicle_id),
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_origin_city (origin_city),
    INDEX idx_destination_city (destination_city),
    INDEX idx_tracking_code (tracking_code),
    INDEX idx_order_number (order_number),
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (driver_id) REFERENCES drivers(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- =====================================================
-- DATOS INICIALES
-- =====================================================

-- Insertar roles iniciales
INSERT IGNORE INTO roles (name, description) VALUES 
('admin', 'Administrador del sistema con todos los permisos'),
('user', 'Usuario regular con permisos limitados');

-- Insertar permisos iniciales
INSERT IGNORE INTO permissions (name, resource, action, description) VALUES 
('users:create', 'users', 'create', 'Crear usuarios'),
('users:read', 'users', 'read', 'Ver usuarios'),
('users:update', 'users', 'update', 'Actualizar usuarios'),
('users:delete', 'users', 'delete', 'Eliminar usuarios'),
('roles:create', 'roles', 'create', 'Crear roles'),
('roles:read', 'roles', 'read', 'Ver roles'),
('roles:update', 'roles', 'update', 'Actualizar roles'),
('roles:delete', 'roles', 'delete', 'Eliminar roles'),
('vehicles:create', 'vehicles', 'create', 'Crear vehículos'),
('vehicles:read', 'vehicles', 'read', 'Ver vehículos'),
('vehicles:update', 'vehicles', 'update', 'Actualizar vehículos'),
('vehicles:delete', 'vehicles', 'delete', 'Eliminar vehículos'),
('drivers:create', 'drivers', 'create', 'Crear conductores'),
('drivers:read', 'drivers', 'read', 'Ver conductores'),
('drivers:update', 'drivers', 'update', 'Actualizar conductores'),
('drivers:delete', 'drivers', 'delete', 'Eliminar conductores'),
('clients:create', 'clients', 'create', 'Crear clientes'),
('clients:read', 'clients', 'read', 'Ver clientes'),
('clients:update', 'clients', 'update', 'Actualizar clientes'),
('clients:delete', 'clients', 'delete', 'Eliminar clientes'),
('orders:create', 'orders', 'create', 'Crear pedidos'),
('orders:read', 'orders', 'read', 'Ver pedidos'),
('orders:update', 'orders', 'update', 'Actualizar pedidos'),
('orders:delete', 'orders', 'delete', 'Eliminar pedidos');

-- Asignar todos los permisos al rol admin
INSERT IGNORE INTO role_permissions (role_id, permission_id) 
SELECT r.id, p.id FROM roles r, permissions p WHERE r.name = 'admin';

-- Asignar permisos limitados al rol user
INSERT IGNORE INTO role_permissions (role_id, permission_id) 
SELECT r.id, p.id FROM roles r, permissions p 
WHERE r.name = 'user' AND p.name IN (
    'vehicles:read', 'drivers:read', 'clients:read', 'orders:read',
    'orders:create', 'orders:update'
);

-- Insertar usuario admin
-- Contraseña: Admin123* (hash: $2b$12$DINTkisqdzoX4385PHhVg.1ORQ1ijlXUgoqKzURhsg8z/NxsRz6Na)
INSERT IGNORE INTO users (username, password_hash, role_id, is_active, security_question1, security_answer1_hash, security_question2, security_answer2_hash) 
VALUES ('admin', '$2b$12$DINTkisqdzoX4385PHhVg.1ORQ1ijlXUgoqKzURhsg8z/NxsRz6Na', 1, 1, '¿Cuál es el nombre de tu primera mascota?', '$2b$12$example1', '¿En qué ciudad naciste?', '$2b$12$example2');

-- =====================================================
-- DATOS DE EJEMPLO
-- =====================================================

-- Datos de ejemplo para vehículos
INSERT IGNORE INTO vehicles (license_plate, brand, model, year, vehicle_type, status) VALUES
('ABC-123', 'Toyota', 'Hilux', 2020, 'camioneta', 'disponible'),
('XYZ-789', 'Ford', 'Transit', 2019, 'furgon', 'disponible'),
('DEF-456', 'Honda', 'CB250', 2021, 'motocicleta', 'disponible');

-- Datos de ejemplo para conductores
INSERT IGNORE INTO drivers (first_name, last_name, email, phone, document_number, license_type, status) VALUES
('Juan', 'Pérez', 'juan.perez@email.com', '3001234567', '12345678', 'B', 'disponible'),
('María', 'García', 'maria.garcia@email.com', '3007654321', '87654321', 'C', 'disponible'),
('Carlos', 'López', 'carlos.lopez@email.com', '3009876543', '11223344', 'A', 'disponible');

-- Datos de ejemplo para clientes
INSERT IGNORE INTO clients (name, email, phone, company, client_type, status) VALUES
('Empresa ABC', 'contacto@empresaabc.com', '6012345678', 'ABC S.A.S.', 'empresa', 'activo'),
('Ana Martínez', 'ana.martinez@email.com', '3001112222', NULL, 'individual', 'activo'),
('Distribuidora XYZ', 'ventas@distribuidoraxyz.com', '6018765432', 'XYZ Distribuciones', 'empresa', 'activo');

-- Datos de ejemplo para pedidos
INSERT IGNORE INTO orders (order_number, client_id, driver_id, vehicle_id, origin_address, destination_address, origin_city, destination_city, description, weight, value, status, priority) VALUES
('ORD-20241026-0001', 1, 1, 1, 'Calle 100 #15-20, Bogotá', 'Carrera 7 #32-10, Medellín', 'Bogotá', 'Medellín', 'Envío de documentos importantes', 2.5, 50000.00, 'pendiente', 'alta'),
('ORD-20241026-0002', 2, 2, 2, 'Carrera 7 #32-10, Medellín', 'Avenida 68 #25-40, Cali', 'Medellín', 'Cali', 'Paquete de productos electrónicos', 15.0, 250000.00, 'asignado', 'media'),
('ORD-20241026-0003', 3, NULL, NULL, 'Avenida 68 #25-40, Cali', 'Calle 100 #15-20, Bogotá', 'Cali', 'Bogotá', 'Mercancía general', 8.0, 120000.00, 'pendiente', 'baja');

-- 01_add_security_questions.sql
ALTER TABLE users
  ADD COLUMN security_question1 VARCHAR(255),
  ADD COLUMN security_answer1_hash VARCHAR(255),
  ADD COLUMN security_question2 VARCHAR(255),  
  ADD COLUMN security_answer2_hash VARCHAR(255);

-- Tabla de auditoría
CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    actor_id INT NULL,
    event_type VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    ip_address VARCHAR(50) NOT NULL,
    extra_data TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);





('ORD-20241026-0003', 3, NULL, NULL, 'Avenida 68 #25-40, Cali', 'Calle 100 #15-20, Bogotá', 'Cali', 'Bogotá', 'Mercancía general', 8.0, 120000.00, 'pendiente', 'baja');
