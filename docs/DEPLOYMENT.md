# 🚀 Guía de Despliegue - Sistema de Rutas Logísticas

Guía completa para desplegar el sistema de gestión logística en diferentes entornos.

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Despliegue con Docker (Recomendado)](#despliegue-con-docker-recomendado)
4. [Despliegue Local sin Docker](#despliegue-local-sin-docker)
5. [Despliegue en Producción](#despliegue-en-producción)
6. [Configuración de Base de Datos](#configuración-de-base-de-datos)
7. [Monitoreo y Logs](#monitoreo-y-logs)
8. [Backup y Recuperación](#backup-y-recuperación)
9. [Troubleshooting](#troubleshooting)

## 🎯 Introducción

El sistema de rutas logísticas está diseñado para ser simple de desplegar y mantener. Esta guía cubre todos los métodos de despliegue disponibles.

## 💻 Requisitos del Sistema

### Mínimos
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Disco**: 10 GB
- **OS**: Windows 10+, Ubuntu 18.04+, macOS 10.14+

### Recomendados
- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Disco**: 20+ GB SSD
- **OS**: Ubuntu 22.04 LTS

### Software Requerido
- **Docker** y **Docker Compose** (recomendado)
- **Python 3.11+** (solo para despliegue local)
- **MySQL 8.0+** (solo para despliegue local)

## 🐳 Despliegue con Docker (Recomendado)

### Instalación Rápida

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd rutasLogisticas
   ```

2. **Ejecutar la aplicación**
   ```bash
   docker-compose up -d
   ```

3. **Verificar funcionamiento**
   ```bash
   curl http://localhost:8000/health
   ```

### Configuración Avanzada

#### Variables de Entorno

Crea un archivo `.env` personalizado:

```env
# Base de datos
DB_HOST=mysql
DB_PORT=3306
DB_NAME=rutas_logisticas
DB_USER=root
DB_PASSWORD=tu_password_seguro

# Aplicación
DEBUG=False
LOG_LEVEL=INFO
```

#### Personalizar Puertos

Modifica `docker-compose.yml`:

```yaml
services:
  app:
    ports:
      - "8001:8000"  # Cambiar puerto externo
  
  mysql:
    ports:
      - "3308:3306"  # Cambiar puerto MySQL
```

### Comandos Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Reiniciar aplicación
docker-compose restart app

# Detener servicios
docker-compose down

# Limpiar todo (¡CUIDADO! Borra datos)
docker-compose down -v
```

## 🖥️ Despliegue Local sin Docker

### Instalación de Dependencias

1. **Instalar Python 3.11+**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3.11 python3.11-venv python3.11-pip

   # Windows
   # Descargar desde python.org
   ```

2. **Crear entorno virtual**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

### Configuración de MySQL

1. **Instalar MySQL**
   ```bash
   # Ubuntu/Debian
   sudo apt install mysql-server

   # Windows
   # Descargar MySQL Installer
   ```

2. **Crear base de datos**
   ```bash
   mysql -u root -p
   CREATE DATABASE rutas_logisticas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **Importar datos iniciales**
   ```bash
   mysql -u root -p rutas_logisticas < database/init_mysql.sql
   ```

### Configuración de la Aplicación

1. **Crear archivo `.env`**
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=rutas_logisticas
   DB_USER=root
   DB_PASSWORD=tu_password
   DEBUG=True
   ```

2. **Ejecutar la aplicación**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🌐 Despliegue en Producción

### Preparación del Servidor

1. **Actualizar sistema**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Instalar Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

3. **Instalar Docker Compose**
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

### Configuración de Producción

1. **Clonar repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd rutasLogisticas
   ```

2. **Configurar variables de entorno**
   ```bash
   cp env.example .env
   nano .env  # Editar con valores de producción
   ```

3. **Configurar firewall**
   ```bash
   sudo ufw allow 22    # SSH
   sudo ufw allow 80    # HTTP
   sudo ufw allow 443   # HTTPS
   sudo ufw enable
   ```

4. **Ejecutar en producción**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

### Configuración de Nginx (Opcional)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🗄️ Configuración de Base de Datos

### Estructura de Datos

El sistema incluye 4 tablas principales:

- **vehicles**: Información de vehículos
- **drivers**: Información de conductores
- **clients**: Información de clientes
- **addresses**: Direcciones de clientes

### Datos de Ejemplo

El sistema incluye datos de prueba:
- 3 vehículos (Toyota, Ford, Honda)
- 3 conductores (Juan, María, Carlos)
- 3 clientes (Empresa ABC, Ana, Distribuidora XYZ)
- 3 direcciones (Bogotá, Medellín, Cali)

### Backup de Base de Datos

```bash
# Con Docker
docker-compose exec mysql mysqldump -u root -p1234 rutas_logisticas > backup.sql

# Restaurar backup
docker-compose exec -T mysql mysql -u root -p1234 rutas_logisticas < backup.sql

# Local
mysqldump -u root -p rutas_logisticas > backup.sql
mysql -u root -p rutas_logisticas < backup.sql
```

## 📊 Monitoreo y Logs

### Ver Logs de la Aplicación

```bash
# Docker
docker-compose logs -f app

# Local
tail -f logs/app.log
```

### Verificar Estado de Servicios

```bash
# Docker
docker-compose ps

# Local
systemctl status mysql
ps aux | grep uvicorn
```

### Health Checks

```bash
# Verificar aplicación
curl http://localhost:8000/health

# Verificar base de datos
docker-compose exec mysql mysqladmin ping -h localhost -u root -p1234
```

## 💾 Backup y Recuperación

### Backup Automático

Crear script de backup:

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
mkdir -p $BACKUP_DIR

# Backup de base de datos
docker-compose exec mysql mysqldump -u root -p1234 rutas_logisticas > $BACKUP_DIR/backup_$DATE.sql

# Backup de archivos de configuración
cp docker-compose.yml $BACKUP_DIR/
cp .env $BACKUP_DIR/

# Mantener solo últimos 7 backups
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

### Recuperación

```bash
# Restaurar desde backup
docker-compose exec -T mysql mysql -u root -p1234 rutas_logisticas < backup_20231201_120000.sql

# Recrear contenedores
docker-compose down
docker-compose up -d
```

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. Puerto 3306 en Uso
```bash
# Error: Puerto 3306 ya está en uso
# Solución: Usar puerto 3307 en docker-compose.yml
mysql -h localhost -P 3307 -u root -p1234
```

#### 2. Aplicación No Inicia
```bash
# Verificar logs
docker-compose logs app

# Verificar que MySQL esté listo
docker-compose logs mysql

# Reiniciar aplicación
docker-compose restart app
```

#### 3. Base de Datos No Conecta
```bash
# Verificar estado de MySQL
docker-compose ps mysql

# Probar conexión
docker-compose exec app python -c "from app.core.database import db_manager; print('DB OK')"
```

#### 4. Permisos de Docker
```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
# Reiniciar sesión
```

### Comandos de Diagnóstico

```bash
# Ver uso de recursos
docker stats

# Ver espacio en disco
df -h

# Ver memoria disponible
free -h

# Ver procesos de Docker
docker ps -a
```

### Logs Importantes

```bash
# Logs de aplicación
docker-compose logs app

# Logs de MySQL
docker-compose logs mysql

# Logs del sistema
journalctl -u docker
```

## 📞 Soporte

Para soporte técnico:

1. Verificar logs de la aplicación
2. Revisar esta guía de troubleshooting
3. Consultar la documentación de la API
4. Contactar al equipo de desarrollo

---

**¡Sistema listo para producción! 🚀**