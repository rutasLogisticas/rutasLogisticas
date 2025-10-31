-- Script simple para agregar columnas de seguridad a la tabla users
USE rutas_logisticas;

-- Agregar columnas de seguridad (ignorar error si ya existen)
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS security_question1 VARCHAR(255) NULL,
ADD COLUMN IF NOT EXISTS security_answer1_hash VARCHAR(255) NULL,
ADD COLUMN IF NOT EXISTS security_question2 VARCHAR(255) NULL,
ADD COLUMN IF NOT EXISTS security_answer2_hash VARCHAR(255) NULL;

-- Si MySQL no soporta IF NOT EXISTS en ALTER TABLE, usar este enfoque:
-- Primero verificar estructura actual
-- DESCRIBE users;

