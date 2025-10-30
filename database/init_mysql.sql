-- Script simple de inicialización
CREATE DATABASE IF NOT EXISTS rutas_logisticas 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE rutas_logisticas;

-- Tabla simple de vehículos
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

-- Tabla simple de conductores
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

-- Tabla simple de clientes
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

-- Tabla para usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


-- Datos de ejemplo
INSERT INTO vehicles (license_plate, brand, model, year, vehicle_type, status) VALUES
('ABC-123', 'Toyota', 'Hilux', 2020, 'camioneta', 'disponible'),
('XYZ-789', 'Ford', 'Transit', 2019, 'furgon', 'disponible'),
('DEF-456', 'Honda', 'CB250', 2021, 'motocicleta', 'disponible');

INSERT INTO drivers (first_name, last_name, email, phone, document_number, license_type, status) VALUES
('Juan', 'Pérez', 'juan.perez@email.com', '3001234567', '12345678', 'B', 'disponible'),
('María', 'García', 'maria.garcia@email.com', '3007654321', '87654321', 'C', 'disponible'),
('Carlos', 'López', 'carlos.lopez@email.com', '3009876543', '11223344', 'A', 'disponible');

INSERT INTO clients (name, email, phone, company, client_type, status) VALUES
('Empresa ABC', 'contacto@empresaabc.com', '6012345678', 'ABC S.A.S.', 'empresa', 'activo'),
('Ana Martínez', 'ana.martinez@email.com', '3001112222', NULL, 'individual', 'activo'),
('Distribuidora XYZ', 'ventas@distribuidoraxyz.com', '6018765432', 'XYZ Distribuciones', 'empresa', 'activo');

-- Tabla de pedidos simplificada
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

-- Datos de ejemplo para pedidos
INSERT INTO orders (order_number, client_id, driver_id, vehicle_id, origin_address, destination_address, origin_city, destination_city, description, weight, value, status, priority) VALUES
('ORD-20241026-0001', 1, 1, 1, 'Calle 100 #15-20, Bogotá', 'Carrera 7 #32-10, Medellín', 'Bogotá', 'Medellín', 'Envío de documentos importantes', 2.5, 50000.00, 'pendiente', 'alta'),
('ORD-20241026-0002', 2, 2, 2, 'Carrera 7 #32-10, Medellín', 'Avenida 68 #25-40, Cali', 'Medellín', 'Cali', 'Paquete de productos electrónicos', 15.0, 250000.00, 'asignado', 'media'),
('ORD-20241026-0003', 3, NULL, NULL, 'Avenida 68 #25-40, Cali', 'Calle 100 #15-20, Bogotá', 'Cali', 'Bogotá', 'Mercancía general', 8.0, 120000.00, 'pendiente', 'baja');

-- 01_add_security_questions.sql
ALTER TABLE users
  ADD COLUMN security_question1 VARCHAR(255),
  ADD COLUMN security_answer1_hash VARCHAR(255),
  ADD COLUMN security_question2 VARCHAR(255),  
  ADD COLUMN security_answer2_hash VARCHAR(255);
