# Guía de Despliegue - Rutas Logísticas

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Configuración de Entorno](#configuración-de-entorno)
4. [Despliegue en Desarrollo](#despliegue-en-desarrollo)
5. [Despliegue en Producción](#despliegue-en-producción)
6. [Configuración de Base de Datos](#configuración-de-base-de-datos)
7. [Configuración de Servidor Web](#configuración-de-servidor-web)
8. [Monitoreo y Logs](#monitoreo-y-logs)
9. [Backup y Recuperación](#backup-y-recuperación)
10. [Seguridad](#seguridad)
11. [Troubleshooting](#troubleshooting)

## Introducción

Esta guía proporciona instrucciones detalladas para desplegar el sistema Rutas Logísticas en diferentes entornos, desde desarrollo local hasta producción.

## Requisitos del Sistema

### Mínimos
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Disco**: 20 GB
- **OS**: Ubuntu 20.04+, CentOS 8+, o Windows Server 2019+

### Recomendados
- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Disco**: 50+ GB SSD
- **OS**: Ubuntu 22.04 LTS

### Software Requerido
- Python 3.11+
- MySQL 8.0+
- Nginx (para producción)
- Docker (opcional)

## Configuración de Entorno

### Variables de Entorno

Crear archivo `.env` basado en `env.example`:

```bash
# Configuración de la aplicación
DEBUG=False
SECRET_KEY=your-production-secret-key-here
API_HOST=0.0.0.0
API_PORT=8000

# Configuración de CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Configuración de base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=rutas_logisticas
DB_USER=rutas_app
DB_PASSWORD=your-secure-db-password
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30

# Configuración de logging
LOG_LEVEL=INFO

# Configuración de seguridad
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SSL_REDIRECT=True
```

### Configuración de Base de Datos

```bash
# Crear usuario de base de datos MySQL
sudo mysql -u root -p
CREATE USER 'rutas_app'@'localhost' IDENTIFIED BY 'your-secure-db-password';
CREATE DATABASE rutas_logisticas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON rutas_logisticas.* TO 'rutas_app'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Configurar MySQL para conexiones
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# Cambiar: bind-address = 127.0.0.1
# Cambiar: port = 3306

sudo systemctl restart mysql
```

## Despliegue en Desarrollo

### Opción 1: Docker Compose (Recomendado)

```bash
# Clonar repositorio
git clone <repository-url>
cd rutas-logisticas

# Configurar entorno
cp env.example .env
# Editar .env con configuraciones de desarrollo

# Iniciar servicios
docker-compose up -d

# Verificar estado
docker-compose ps
docker-compose logs app
```

### Opción 2: Instalación Manual

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
createdb rutas_logisticas
psql -d rutas_logisticas -f database/init.sql

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Verificar Instalación

```bash
# Verificar API
curl http://localhost:8000/health

# Verificar documentación
# Abrir http://localhost:8000/docs en el navegador
```

## Despliegue en Producción

### Opción 1: Docker Compose

```bash
# Crear archivo de producción
cp docker-compose.yml docker-compose.prod.yml

# Editar docker-compose.prod.yml
version: '3.8'
services:
  app:
    build: .
    environment:
      - DEBUG=False
      - DB_HOST=mysql
      - DB_PASSWORD=${DB_PASSWORD}
    restart: unless-stopped
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 1G
          cpus: '0.5'

# Iniciar en producción
docker-compose -f docker-compose.prod.yml up -d
```

### Opción 2: Instalación en Servidor

#### 1. Preparar Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3.11 python3.11-venv python3-pip mysql-server nginx

# Crear usuario de aplicación
sudo useradd -m -s /bin/bash rutas
sudo usermod -aG sudo rutas
```

#### 2. Configurar Aplicación

```bash
# Cambiar a usuario de aplicación
sudo su - rutas

# Clonar código
git clone <repository-url> /home/rutas/rutas-logisticas
cd /home/rutas/rutas-logisticas

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 3. Configurar Base de Datos

```bash
# Como root user de MySQL
sudo mysql -u root -p

# Crear base de datos y usuario
CREATE DATABASE rutas_logisticas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'rutas_app'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON rutas_logisticas.* TO 'rutas_app'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Ejecutar script de inicialización
mysql -u rutas_app -p rutas_logisticas < database/init_mysql.sql

# Ejecutar migraciones
alembic upgrade head
```

#### 4. Configurar Systemd Service

```bash
sudo nano /etc/systemd/system/rutas-logisticas.service
```

```ini
[Unit]
Description=Rutas Logísticas API
After=network.target mysql.service

[Service]
Type=exec
User=rutas
Group=rutas
WorkingDirectory=/home/rutas/rutas-logisticas
Environment=PATH=/home/rutas/rutas-logisticas/venv/bin
ExecStart=/home/rutas/rutas-logisticas/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar y iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable rutas-logisticas
sudo systemctl start rutas-logisticas
sudo systemctl status rutas-logisticas
```

#### 5. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/rutas-logisticas
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirección HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # Certificados SSL
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Configuración SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;

    # Headers de seguridad
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Proxy a la aplicación
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # Archivos estáticos
    location /static/ {
        alias /home/rutas/rutas-logisticas/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/rutas-logisticas /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 6. Configurar SSL con Let's Encrypt

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Configurar renovación automática
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Configuración de Base de Datos

### Optimización de MySQL

```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

```conf
# Configuraciones de memoria
innodb_buffer_pool_size = 256M
query_cache_size = 64M
query_cache_limit = 2M

# Configuraciones de conexión
max_connections = 100
bind-address = 0.0.0.0

# Configuraciones de logging
general_log = 1
general_log_file = /var/log/mysql/general.log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 1

# Configuraciones de InnoDB
innodb_log_file_size = 64M
innodb_log_buffer_size = 16M
innodb_flush_log_at_trx_commit = 1
```

### Backup Automático

```bash
# Script de backup
sudo nano /usr/local/bin/backup_rutas_db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/rutas_logisticas"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="rutas_logisticas"
DB_USER="rutas_app"

mkdir -p $BACKUP_DIR

# Backup completo
pg_dump -h localhost -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/rutas_${DATE}.sql.gz

# Limpiar backups antiguos (mantener últimos 7 días)
find $BACKUP_DIR -name "rutas_*.sql.gz" -mtime +7 -delete

echo "Backup completado: rutas_${DATE}.sql.gz"
```

```bash
# Hacer ejecutable
sudo chmod +x /usr/local/bin/backup_rutas_db.sh

# Programar backup diario
sudo crontab -e
# Agregar: 0 2 * * * /usr/local/bin/backup_rutas_db.sh
```

## Configuración de Servidor Web

### Nginx - Configuraciones Avanzadas

```nginx
# Configuración de rate limiting
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://127.0.0.1:8000;
        }
    }
}

# Configuración de compresión
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

# Configuración de cache
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Monitoreo y Logs

### Configuración de Logs

```python
# En app/core/config.py
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/rutas-logisticas/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'detailed'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
```

### Monitoreo con Prometheus

```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## Backup y Recuperación

### Backup Completo del Sistema

```bash
#!/bin/bash
# Script de backup completo
BACKUP_DIR="/var/backups/rutas_logisticas/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup de base de datos
pg_dump -h localhost -U rutas_app rutas_logisticas | gzip > $BACKUP_DIR/database.sql.gz

# Backup de código
tar -czf $BACKUP_DIR/code.tar.gz /home/rutas/rutas-logisticas

# Backup de configuración
tar -czf $BACKUP_DIR/config.tar.gz /etc/nginx/sites-available/rutas-logisticas /etc/systemd/system/rutas-logisticas.service

echo "Backup completo guardado en: $BACKUP_DIR"
```

### Procedimiento de Recuperación

```bash
# 1. Restaurar base de datos
gunzip -c /var/backups/rutas_logisticas/20240101/database.sql.gz | psql -h localhost -U rutas_app rutas_logisticas

# 2. Restaurar código
tar -xzf /var/backups/rutas_logisticas/20240101/code.tar.gz -C /

# 3. Restaurar configuración
tar -xzf /var/backups/rutas_logisticas/20240101/config.tar.gz -C /

# 4. Reiniciar servicios
sudo systemctl restart rutas-logisticas
sudo systemctl restart nginx
```

## Seguridad

### Configuraciones de Seguridad

#### 1. Firewall

```bash
# Configurar UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

#### 2. Fail2Ban

```bash
# Instalar Fail2Ban
sudo apt install -y fail2ban

# Configurar para Nginx
sudo nano /etc/fail2ban/jail.local
```

```ini
[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
```

#### 3. Actualizaciones Automáticas

```bash
# Configurar actualizaciones automáticas
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### Configuraciones de Aplicación

```python
# En app/core/config.py
SECURITY_CONFIG = {
    'CORS_ORIGINS': ['https://yourdomain.com'],
    'ALLOWED_HOSTS': ['yourdomain.com', 'www.yourdomain.com'],
    'SECURE_SSL_REDIRECT': True,
    'SECURE_HSTS_SECONDS': 31536000,
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
    'SECURE_HSTS_PRELOAD': True,
    'SECURE_CONTENT_TYPE_NOSNIFF': True,
    'SECURE_BROWSER_XSS_FILTER': True,
    'X_FRAME_OPTIONS': 'DENY'
}
```

## Troubleshooting

### Problemas Comunes

#### 1. Error de Conexión a Base de Datos

```bash
# Verificar estado de MySQL
sudo systemctl status mysql

# Verificar conexión
mysql -h localhost -u rutas_app -p rutas_logisticas

# Verificar logs
sudo tail -f /var/log/mysql/error.log
```

#### 2. Error de Permisos

```bash
# Verificar permisos de archivos
ls -la /home/rutas/rutas-logisticas/

# Corregir permisos
sudo chown -R rutas:rutas /home/rutas/rutas-logisticas/
sudo chmod -R 755 /home/rutas/rutas-logisticas/
```

#### 3. Error de Puerto en Uso

```bash
# Verificar puertos en uso
sudo netstat -tulpn | grep :8000

# Matar proceso si es necesario
sudo kill -9 <PID>
```

#### 4. Error de SSL

```bash
# Verificar certificados
sudo certbot certificates

# Renovar certificados
sudo certbot renew --dry-run
```

### Logs de Diagnóstico

```bash
# Logs de aplicación
sudo journalctl -u rutas-logisticas -f

# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs de MySQL
sudo tail -f /var/log/mysql/error.log
```

### Comandos de Diagnóstico

```bash
# Verificar estado de servicios
sudo systemctl status rutas-logisticas nginx mysql

# Verificar conectividad
curl -I http://localhost:8000/health
curl -I https://yourdomain.com/health

# Verificar base de datos
mysql -u root -p -e "SELECT VERSION();"
mysql -u rutas_app -p rutas_logisticas -e "SELECT COUNT(*) FROM vehicles;"

# Verificar recursos del sistema
htop
df -h
free -h
```

### Contacto de Soporte

Para soporte técnico:
- 📧 Email: devops@empresa.com
- 🐛 Issues: [GitHub Issues](https://github.com/empresa/rutas-logisticas/issues)
- 📖 Wiki: [Documentación del Proyecto](https://github.com/empresa/rutas-logisticas/wiki)
