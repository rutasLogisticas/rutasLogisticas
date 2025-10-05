# 🐳 Guía de Docker - Sistema de Rutas Logísticas

Esta guía explica cómo ejecutar y gestionar el sistema de rutas logísticas usando Docker.

## 🚀 Inicio Rápido

### Ejecutar la Aplicación

```bash
# Construir y ejecutar todos los servicios
docker-compose up -d --build

# Ver logs en tiempo real
docker-compose logs -f

# Verificar estado de los contenedores
docker-compose ps
```

### Verificar que Funciona

```bash
# Health check
curl http://localhost:8000/health

# Listar vehículos
curl http://localhost:8000/api/v1/vehicles
```

## 🏗️ Servicios Docker

### Aplicación FastAPI
- **Puerto**: 8000
- **Imagen**: rutaslogisticas-app:latest
- **Variables**: Configuradas en docker-compose.yml

### Base de Datos MySQL
- **Puerto**: 3307 (externa), 3306 (interna)
- **Usuario**: root
- **Contraseña**: 1234
- **Base de datos**: rutas_logisticas
- **Volumen**: rutaslogisticas_mysql_data

### Redis (Opcional)
- **Puerto**: 6379
- **Uso**: Cache de la aplicación

## 📋 Comandos Útiles

### Gestión de Contenedores

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Reiniciar un servicio específico
docker-compose restart app

# Ver logs de un servicio
docker-compose logs app
docker-compose logs mysql
```

### Base de Datos

```bash
# Acceder a MySQL desde el host
mysql -h localhost -P 3307 -u root -p1234 rutas_logisticas

# Acceder a MySQL desde dentro del contenedor
docker-compose exec mysql mysql -u root -p1234 rutas_logisticas

# Ver estructura de tablas
docker-compose exec mysql mysql -u root -p1234 -e "SHOW TABLES;" rutas_logisticas
```

### Limpieza

```bash
# Detener y eliminar contenedores, redes y volúmenes
docker-compose down -v

# Eliminar imágenes
docker-compose down --rmi all

# Limpieza completa del sistema Docker
docker system prune -a
```

## 🔧 Configuración

### Variables de Entorno

Las variables están configuradas en `docker-compose.yml`:

```yaml
environment:
  - DB_HOST=mysql
  - DB_PORT=3306
  - DB_NAME=rutas_logisticas
  - DB_USER=root
  - DB_PASSWORD=1234
  - DEBUG=True
```

### Volúmenes

- **mysql_data**: Persistencia de la base de datos
- **app**: Código fuente de la aplicación

### Redes

- **rutas_network**: Red interna para comunicación entre servicios

## 🐛 Troubleshooting

### Problemas Comunes

#### Puerto 3306 en Uso
```bash
# Error: Puerto 3306 ya está en uso
# Solución: El puerto externo está configurado como 3307
mysql -h localhost -P 3307 -u root -p1234
```

#### Aplicación No Inicia
```bash
# Verificar logs
docker-compose logs app

# Verificar que MySQL esté listo
docker-compose logs mysql

# Reiniciar aplicación
docker-compose restart app
```

#### Base de Datos No Conecta
```bash
# Verificar que MySQL esté corriendo
docker-compose ps mysql

# Verificar logs de MySQL
docker-compose logs mysql

# Probar conexión
docker-compose exec app python -c "from app.core.database import db_manager; print('DB OK')"
```

### Logs Importantes

```bash
# Ver logs de la aplicación
docker-compose logs -f app

# Ver logs de MySQL
docker-compose logs -f mysql

# Ver logs de todos los servicios
docker-compose logs -f
```

## 📊 Monitoreo

### Estado de Servicios

```bash
# Ver estado de todos los servicios
docker-compose ps

# Ver uso de recursos
docker stats

# Ver información detallada de un contenedor
docker-compose exec app ps aux
```

### Health Checks

```bash
# Health check de la aplicación
curl http://localhost:8000/health

# Verificar endpoints principales
curl http://localhost:8000/api/v1/vehicles
curl http://localhost:8000/api/v1/drivers
curl http://localhost:8000/api/v1/clients
curl http://localhost:8000/api/v1/addresses
```

## 🔄 Actualizaciones

### Actualizar Código

```bash
# Detener servicios
docker-compose down

# Reconstruir con cambios
docker-compose up -d --build

# O solo reconstruir la aplicación
docker-compose build app
docker-compose up -d app
```

### Actualizar Base de Datos

```bash
# Hacer backup de la base de datos
docker-compose exec mysql mysqldump -u root -p1234 rutas_logisticas > backup.sql

# Restaurar backup
docker-compose exec -T mysql mysql -u root -p1234 rutas_logisticas < backup.sql
```

## 🌐 Acceso desde Otras Máquinas

Para acceder desde otras máquinas en la red:

```bash
# Cambiar localhost por la IP de la máquina
curl http://192.168.1.100:8000/health
```

## 📝 Notas Importantes

1. **Puerto MySQL**: Se expone en 3307 para evitar conflictos
2. **Datos Persistentes**: La base de datos se mantiene entre reinicios
3. **Logs**: Los logs se pueden ver en tiempo real con `docker-compose logs -f`
4. **Variables**: Configuradas para desarrollo, cambiar para producción

## 🚀 Producción

Para producción, considera:

1. Cambiar contraseñas por defecto
2. Usar volúmenes externos para datos
3. Configurar backups automáticos
4. Implementar monitoreo
5. Usar HTTPS/TLS
6. Configurar firewall apropiadamente

---

**¡El sistema está listo para usar con Docker! 🎉**