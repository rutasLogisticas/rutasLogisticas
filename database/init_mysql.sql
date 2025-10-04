-- Script de inicialización de base de datos para Rutas Logísticas - MySQL
-- Implementa las tablas y relaciones del sistema

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS rutas_logisticas 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE rutas_logisticas;

-- Tabla de vehículos
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INT NOT NULL CHECK (year >= 1900 AND year <= 2030),
    color VARCHAR(50),
    vehicle_type ENUM('camion', 'furgon', 'motocicleta', 'bicicleta', 'camioneta') NOT NULL,
    status ENUM('disponible', 'en_ruta', 'mantenimiento', 'fuera_servicio') DEFAULT 'disponible',
    capacity_weight DECIMAL(10,2) CHECK (capacity_weight > 0),
    capacity_volume DECIMAL(10,2) CHECK (capacity_volume > 0),
    fuel_type VARCHAR(50),
    fuel_consumption DECIMAL(5,2) CHECK (fuel_consumption > 0),
    last_maintenance VARCHAR(50),
    next_maintenance VARCHAR(50),
    insurance_expiry VARCHAR(50),
    notes TEXT,
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
    address TEXT,
    document_type VARCHAR(20) DEFAULT 'DNI',
    document_number VARCHAR(20) UNIQUE NOT NULL,
    birth_date DATE,
    employee_id VARCHAR(50) UNIQUE,
    hire_date DATE,
    salary INT CHECK (salary >= 0),
    status ENUM('disponible', 'en_ruta', 'descansando', 'vacaciones', 'fuera_servicio') DEFAULT 'disponible',
    license_type ENUM('A', 'B', 'C', 'D', 'E') NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    license_expiry DATE NOT NULL,
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    notes TEXT,
    is_available BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    client_type ENUM('persona_natural', 'empresa', 'organizacion') NOT NULL,
    status ENUM('activo', 'inactivo', 'suspendido', 'potencial') DEFAULT 'activo',
    email VARCHAR(255),
    phone VARCHAR(20),
    secondary_phone VARCHAR(20),
    website VARCHAR(255),
    tax_id VARCHAR(50) UNIQUE,
    business_name VARCHAR(255),
    main_address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Ecuador',
    postal_code VARCHAR(20),
    contact_person VARCHAR(255),
    contact_position VARCHAR(100),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    credit_limit DECIMAL(12,2) DEFAULT 0.0 CHECK (credit_limit >= 0),
    payment_terms INT DEFAULT 30 CHECK (payment_terms >= 0),
    discount_percentage DECIMAL(5,2) DEFAULT 0.0 CHECK (discount_percentage >= 0 AND discount_percentage <= 100),
    notes TEXT,
    internal_notes TEXT,
    tags VARCHAR(500),
    receives_notifications BOOLEAN DEFAULT TRUE,
    is_priority BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tabla de direcciones
CREATE TABLE IF NOT EXISTS addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    address_type ENUM('domicilio', 'oficina', 'almacen', 'entrega', 'recogida', 'facturacion', 'otro') NOT NULL,
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    neighborhood VARCHAR(100),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) DEFAULT 'Ecuador',
    postal_code VARCHAR(20),
    latitude DECIMAL(10, 8) CHECK (latitude >= -90 AND latitude <= 90),
    longitude DECIMAL(11, 8) CHECK (longitude >= -180 AND longitude <= 180),
    reference_points TEXT,
    delivery_instructions TEXT,
    contact_name VARCHAR(255),
    contact_phone VARCHAR(20),
    access_notes TEXT,
    parking_available BOOLEAN DEFAULT TRUE,
    delivery_time_preference VARCHAR(100),
    is_primary BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_delivery_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Índices para optimizar consultas
CREATE INDEX idx_vehicles_license_plate ON vehicles(license_plate);
CREATE INDEX idx_vehicles_type ON vehicles(vehicle_type);
CREATE INDEX idx_vehicles_status ON vehicles(status);
CREATE INDEX idx_vehicles_available ON vehicles(is_available);
CREATE INDEX idx_vehicles_active ON vehicles(is_active);

CREATE INDEX idx_drivers_email ON drivers(email);
CREATE INDEX idx_drivers_document ON drivers(document_number);
CREATE INDEX idx_drivers_license ON drivers(license_number);
CREATE INDEX idx_drivers_employee_id ON drivers(employee_id);
CREATE INDEX idx_drivers_status ON drivers(status);
CREATE INDEX idx_drivers_license_type ON drivers(license_type);
CREATE INDEX idx_drivers_license_expiry ON drivers(license_expiry);
CREATE INDEX idx_drivers_active ON drivers(is_active);

CREATE INDEX idx_clients_name ON clients(name);
CREATE INDEX idx_clients_email ON clients(email);
CREATE INDEX idx_clients_tax_id ON clients(tax_id);
CREATE INDEX idx_clients_type ON clients(client_type);
CREATE INDEX idx_clients_status ON clients(status);
CREATE INDEX idx_clients_city ON clients(city);
CREATE INDEX idx_clients_state ON clients(state);
CREATE INDEX idx_clients_priority ON clients(is_priority);
CREATE INDEX idx_clients_active ON clients(is_active);

CREATE INDEX idx_addresses_client_id ON addresses(client_id);
CREATE INDEX idx_addresses_type ON addresses(address_type);
CREATE INDEX idx_addresses_city ON addresses(city);
CREATE INDEX idx_addresses_state ON addresses(state);
CREATE INDEX idx_addresses_primary ON addresses(is_primary);
CREATE INDEX idx_addresses_delivery ON addresses(is_delivery_available);
CREATE INDEX idx_addresses_coordinates ON addresses(latitude, longitude);
CREATE INDEX idx_addresses_active ON addresses(is_active);

-- Datos de ejemplo para testing
INSERT INTO vehicles (license_plate, brand, model, year, color, vehicle_type, capacity_weight, capacity_volume, fuel_type, fuel_consumption) VALUES
('ABC-1234', 'Toyota', 'Hilux', 2022, 'Blanco', 'camioneta', 1000.00, 2.5, 'Diesel', 8.5),
('XYZ-5678', 'Mercedes', 'Sprinter', 2021, 'Azul', 'furgon', 3500.00, 12.0, 'Diesel', 7.2),
('DEF-9012', 'Honda', 'CB 190R', 2023, 'Rojo', 'motocicleta', 150.00, 0.1, 'Gasolina', 3.5);

INSERT INTO drivers (first_name, last_name, email, phone, document_number, license_type, license_number, license_expiry) VALUES
('Juan', 'Pérez', 'juan.perez@empresa.com', '+593991234567', '1234567890', 'C', 'LIC123456', '2025-12-31'),
('María', 'González', 'maria.gonzalez@empresa.com', '+593991234568', '1234567891', 'B', 'LIC123457', '2025-11-30'),
('Carlos', 'Rodríguez', 'carlos.rodriguez@empresa.com', '+593991234569', '1234567892', 'A', 'LIC123458', '2025-10-31');

INSERT INTO clients (name, client_type, email, phone, city, state, contact_person, contact_email) VALUES
('Empresa ABC S.A.', 'empresa', 'contacto@empresaabc.com', '+593221234567', 'Quito', 'Pichincha', 'Ana López', 'ana.lopez@empresaabc.com'),
('Distribuidora XYZ', 'empresa', 'ventas@distribuidoraxyz.com', '+593221234568', 'Guayaquil', 'Guayas', 'Pedro Martínez', 'pedro.martinez@distribuidoraxyz.com'),
('María Fernández', 'persona_natural', 'maria.fernandez@gmail.com', '+593991234570', 'Cuenca', 'Azuay', 'María Fernández', 'maria.fernandez@gmail.com');

INSERT INTO addresses (client_id, address_type, address_line1, city, state, is_primary, latitude, longitude) VALUES
(1, 'oficina', 'Av. Amazonas N12-34', 'Quito', 'Pichincha', TRUE, -0.2298500, -78.5249500),
(1, 'almacen', 'Calle 5 de Junio S12-45', 'Quito', 'Pichincha', FALSE, -0.2350000, -78.5300000),
(2, 'oficina', 'Av. 9 de Octubre 123', 'Guayaquil', 'Guayas', TRUE, -2.1894120, -79.8890660),
(3, 'domicilio', 'Calle Larga 456', 'Cuenca', 'Azuay', TRUE, -2.9001290, -79.0058960);

-- Vistas útiles para consultas frecuentes
CREATE OR REPLACE VIEW v_vehicles_available AS
SELECT 
    id, license_plate, brand, model, year, vehicle_type, status,
    capacity_weight, capacity_volume, fuel_type, fuel_consumption
FROM vehicles 
WHERE is_active = TRUE AND status = 'disponible' AND is_available = TRUE;

CREATE OR REPLACE VIEW v_drivers_available AS
SELECT 
    id, first_name, last_name, email, phone, license_type, license_number,
    license_expiry, status
FROM drivers 
WHERE is_active = TRUE AND status = 'disponible' AND is_available = TRUE 
AND license_expiry > CURDATE();

CREATE OR REPLACE VIEW v_clients_active AS
SELECT 
    id, name, client_type, email, phone, city, state, is_priority,
    contact_person, contact_email
FROM clients 
WHERE is_active = TRUE AND status = 'activo';

CREATE OR REPLACE VIEW v_addresses_delivery AS
SELECT 
    a.id, a.client_id, c.name as client_name, a.address_type,
    a.address_line1, a.city, a.state, a.contact_name, a.contact_phone,
    a.latitude, a.longitude
FROM addresses a
JOIN clients c ON a.client_id = c.id
WHERE a.is_active = TRUE AND a.is_delivery_available = TRUE;

-- Funciones de utilidad
DELIMITER //

CREATE FUNCTION get_driver_age(driver_id INT)
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE birth_date DATE;
    DECLARE age INT;
    
    SELECT drivers.birth_date INTO birth_date 
    FROM drivers 
    WHERE id = driver_id AND is_active = TRUE;
    
    IF birth_date IS NULL THEN
        RETURN NULL;
    END IF;
    
    SET age = YEAR(CURDATE()) - YEAR(birth_date) - 
              (DATE_FORMAT(CURDATE(), '%m%d') < DATE_FORMAT(birth_date, '%m%d'));
    
    RETURN age;
END //

CREATE FUNCTION is_license_expired(driver_id INT)
RETURNS BOOLEAN
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE expiry_date DATE;
    
    SELECT drivers.license_expiry INTO expiry_date 
    FROM drivers 
    WHERE id = driver_id AND is_active = TRUE;
    
    IF expiry_date IS NULL THEN
        RETURN TRUE;
    END IF;
    
    RETURN expiry_date < CURDATE();
END //

DELIMITER ;

-- Comentarios en las tablas
ALTER TABLE vehicles COMMENT = 'Tabla de vehículos de la flota logística';
ALTER TABLE drivers COMMENT = 'Tabla de conductores/choferes';
ALTER TABLE clients COMMENT = 'Tabla de clientes (personas y empresas)';
ALTER TABLE addresses COMMENT = 'Tabla de direcciones asociadas a clientes';

-- Permisos de usuario (ajustar según necesidades)
-- CREATE USER 'rutas_app'@'localhost' IDENTIFIED BY 'secure_password';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON rutas_logisticas.* TO 'rutas_app'@'localhost';
-- FLUSH PRIVILEGES;
