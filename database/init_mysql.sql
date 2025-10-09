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

-- Tabla simple de direcciones
CREATE TABLE IF NOT EXISTS addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    street VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) DEFAULT 'Colombia',
    address_type VARCHAR(20) DEFAULT 'principal',
    is_primary BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
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

INSERT INTO addresses (client_id, street, city, state, postal_code, country, address_type, is_primary) VALUES
(1, 'Calle 100 #15-20', 'Bogotá', 'Cundinamarca', '110111', 'Colombia', 'principal', TRUE),
(2, 'Carrera 7 #32-10', 'Medellín', 'Antioquia', '050001', 'Colombia', 'principal', TRUE),
(3, 'Avenida 68 #25-40', 'Cali', 'Valle del Cauca', '760001', 'Colombia', 'principal', TRUE);