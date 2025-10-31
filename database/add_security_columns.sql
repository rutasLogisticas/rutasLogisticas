-- Script para agregar columnas de seguridad a la tabla users
-- Este script es seguro para ejecutar múltiples veces (usando IF NOT EXISTS no estándar)

USE rutas_logisticas;

-- Verificar y agregar columnas si no existen
SET @dbname = DATABASE();
SET @tablename = 'users';

-- Verificar si la columna security_question1 existe
SET @preparedStatement = (
    SELECT IF(
        (
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
            WHERE (table_name = @tablename)
            AND (table_schema = @dbname)
            AND (column_name = 'security_question1')
        ) > 0,
        'SELECT 1',
        'ALTER TABLE users ADD COLUMN security_question1 VARCHAR(255) NULL AFTER password_hash'
    )
);
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Verificar si la columna security_answer1_hash existe
SET @preparedStatement = (
    SELECT IF(
        (
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
            WHERE (table_name = @tablename)
            AND (table_schema = @dbname)
            AND (column_name = 'security_answer1_hash')
        ) > 0,
        'SELECT 1',
        'ALTER TABLE users ADD COLUMN security_answer1_hash VARCHAR(255) NULL AFTER security_question1'
    )
);
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Verificar si la columna security_question2 existe
SET @preparedStatement = (
    SELECT IF(
        (
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
            WHERE (table_name = @tablename)
            AND (table_schema = @dbname)
            AND (column_name = 'security_question2')
        ) > 0,
        'SELECT 1',
        'ALTER TABLE users ADD COLUMN security_question2 VARCHAR(255) NULL AFTER security_answer1_hash'
    )
);
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Verificar si la columna security_answer2_hash existe
SET @preparedStatement = (
    SELECT IF(
        (
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
            WHERE (table_name = @tablename)
            AND (table_schema = @dbname)
            AND (column_name = 'security_answer2_hash')
        ) > 0,
        'SELECT 1',
        'ALTER TABLE users ADD COLUMN security_answer2_hash VARCHAR(255) NULL AFTER security_question2'
    )
);
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Verificar estructura final
DESCRIBE users;

