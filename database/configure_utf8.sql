-- Script para configurar UTF-8 en MySQL
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET character_set_client = utf8mb4;
SET character_set_connection = utf8mb4;
SET character_set_results = utf8mb4;

-- Configurar la base de datos
ALTER DATABASE rutas_logisticas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Configurar todas las tablas existentes
ALTER TABLE clients CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE drivers CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE vehicles CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE orders CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE users CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Insertar datos de prueba con caracteres especiales
INSERT INTO clients (name, email, phone, company, client_type, status) VALUES
('José María González', 'jose.maria@email.com', '3001234567', 'Empresa Ñoño S.A.S.', 'empresa', 'activo'),
('María José Pérez', 'maria.jose@email.com', '3007654321', NULL, 'individual', 'activo'),
('Álvaro Rodríguez', 'alvaro.rodriguez@email.com', '3009876543', 'Distribuidora Española', 'empresa', 'activo')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO drivers (first_name, last_name, email, phone, document_number, license_type, status) VALUES
('José', 'González', 'jose.gonzalez@email.com', '3001111111', '11111111', 'B', 'disponible'),
('María', 'Fernández', 'maria.fernandez@email.com', '3002222222', '22222222', 'C', 'disponible'),
('Álvaro', 'Martínez', 'alvaro.martinez@email.com', '3003333333', '33333333', 'A', 'disponible')
ON DUPLICATE KEY UPDATE first_name = VALUES(first_name);
