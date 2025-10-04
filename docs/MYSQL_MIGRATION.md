# Migración de PostgreSQL a MySQL

Esta guía explica cómo migrar el sistema Rutas Logísticas de PostgreSQL a MySQL.

## Cambios Realizados

### 1. Dependencias Actualizadas

Se han actualizado las dependencias en `requirements.txt`:

```diff
- psycopg2-binary==2.9.9
+ pymysql==1.1.0
+ cryptography==41.0.8
```

### 2. Configuración de Base de Datos

#### Archivo `app/core/config.py`
- Puerto por defecto cambiado de `5432` a `3306`
- Usuario por defecto cambiado de `postgres` a `root`
- URL de conexión actualizada a `mysql+pymysql://`
- Agregadas configuraciones de charset y collation

#### Archivo `env.example`
```diff
- DB_PORT=5432
- DB_USER=postgres
+ DB_PORT=3306
+ DB_USER=root
+ DB_CHARSET=utf8mb4
+ DB_COLLATION=utf8mb4_unicode_ci
```

### 3. Script SQL

Se ha creado `database/init_mysql.sql` con las siguientes adaptaciones:

#### Diferencias Principales:
- **AUTO_INCREMENT** en lugar de SERIAL
- **ENUM** para tipos de datos con valores limitados
- **ENGINE=InnoDB** especificado
- **CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci**
- **ON UPDATE CURRENT_TIMESTAMP** para updated_at
- Funciones adaptadas a sintaxis MySQL
- Triggers simplificados

#### Ejemplo de Cambio:
```sql
-- PostgreSQL
id SERIAL PRIMARY KEY,
status VARCHAR(20) CHECK (status IN ('activo', 'inactivo')),

-- MySQL
id INT AUTO_INCREMENT PRIMARY KEY,
status ENUM('activo', 'inactivo') DEFAULT 'activo',
```

### 4. Docker Compose

Se han creado dos archivos:

#### `docker-compose.yml` (actualizado)
- Servicio `postgres` cambiado a `mysql`
- Puerto `5432` cambiado a `3306`
- Variables de entorno MySQL
- Script de inicialización actualizado

#### `docker-compose.mysql.yml` (nuevo)
- Configuración completa con MySQL
- Health checks incluidos
- phpMyAdmin para administración
- Configuración optimizada para desarrollo

## Instrucciones de Migración

### Opción 1: Migración Limpia (Recomendada)

1. **Hacer backup de datos existentes** (si los hay):
```bash
# Exportar datos de PostgreSQL
pg_dump -h localhost -U postgres rutas_logisticas > backup_postgres.sql
```

2. **Detener servicios actuales**:
```bash
docker-compose down
```

3. **Cambiar a configuración MySQL**:
```bash
# Usar el archivo específico de MySQL
docker-compose -f docker-compose.mysql.yml up -d
```

4. **Verificar la migración**:
```bash
# Verificar que la aplicación funciona
curl http://localhost:8000/health

# Verificar base de datos
mysql -h localhost -u root -p -e "USE rutas_logisticas; SHOW TABLES;"
```

### Opción 2: Migración con Docker Compose Estándar

1. **Actualizar el archivo principal**:
```bash
# El archivo docker-compose.yml ya está actualizado
docker-compose down
docker-compose up -d
```

2. **Verificar servicios**:
```bash
docker-compose ps
```

### Opción 3: Migración Manual

1. **Instalar MySQL**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# macOS con Homebrew
brew install mysql
brew services start mysql

# Windows
# Descargar desde https://dev.mysql.com/downloads/mysql/
```

2. **Crear base de datos**:
```bash
mysql -u root -p
CREATE DATABASE rutas_logisticas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. **Ejecutar script de inicialización**:
```bash
mysql -u root -p rutas_logisticas < database/init_mysql.sql
```

4. **Configurar variables de entorno**:
```bash
cp env.example .env
# Editar .env con las credenciales correctas
```

5. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

6. **Iniciar aplicación**:
```bash
uvicorn app.main:app --reload
```

## Verificación de la Migración

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Verificar Tablas
```sql
USE rutas_logisticas;
SHOW TABLES;
DESCRIBE vehicles;
DESCRIBE drivers;
DESCRIBE clients;
DESCRIBE addresses;
```

### 3. Verificar Datos de Ejemplo
```sql
SELECT COUNT(*) FROM vehicles;
SELECT COUNT(*) FROM drivers;
SELECT COUNT(*) FROM clients;
SELECT COUNT(*) FROM addresses;
```

### 4. Probar API
```bash
# Listar vehículos
curl http://localhost:8000/api/v1/vehicles

# Listar conductores
curl http://localhost:8000/api/v1/drivers

# Listar clientes
curl http://localhost:8000/api/v1/clients
```

## Diferencias Importantes

### 1. Tipos de Datos
- **PostgreSQL SERIAL** → **MySQL AUTO_INCREMENT**
- **PostgreSQL VARCHAR con CHECK** → **MySQL ENUM**
- **PostgreSQL TIMESTAMP** → **MySQL TIMESTAMP con ON UPDATE**

### 2. Funciones
- **PostgreSQL plpgsql** → **MySQL DELIMITER y funciones nativas**
- **PostgreSQL AGE()** → **MySQL YEAR() y DATE_FORMAT()**
- **PostgreSQL CURRENT_DATE** → **MySQL CURDATE()**

### 3. Características Específicas
- **Charset**: utf8mb4 para soporte completo de Unicode
- **Engine**: InnoDB para transacciones y claves foráneas
- **Autenticación**: mysql_native_password para compatibilidad

## Troubleshooting

### Error de Conexión
```
OperationalError: (pymysql.err.OperationalError) (1045, "Access denied for user 'root'@'localhost'")
```

**Solución**:
```bash
# Resetear contraseña de root
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;
```

### Error de Charset
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Solución**: Verificar que la base de datos use utf8mb4:
```sql
ALTER DATABASE rutas_logisticas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Error de Autenticación en Docker
```
Authentication plugin 'caching_sha2_password' cannot be loaded
```

**Solución**: Usar mysql_native_password en docker-compose:
```yaml
command: --default-authentication-plugin=mysql_native_password
```

## Ventajas de MySQL

1. **Amplia adopción**: MySQL es más común en hosting compartido
2. **Performance**: Optimizado para aplicaciones web
3. **Herramientas**: phpMyAdmin, MySQL Workbench
4. **Compatibilidad**: Mejor soporte en algunos entornos cloud
5. **Licencia**: Más permisiva para algunos casos de uso

## Rollback a PostgreSQL

Si necesitas volver a PostgreSQL:

1. **Restaurar dependencias**:
```bash
# En requirements.txt
psycopg2-binary==2.9.9
```

2. **Restaurar configuración**:
```bash
# En app/core/config.py
port: int = 5432
username: str = "postgres"
```

3. **Usar docker-compose original**:
```bash
docker-compose down
# Restaurar docker-compose.yml original
docker-compose up -d
```

---

**La migración a MySQL mantiene toda la funcionalidad del sistema mientras mejora la compatibilidad y facilita el despliegue en diferentes entornos.**
