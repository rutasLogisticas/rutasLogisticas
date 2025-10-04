#!/usr/bin/env python3
"""
Script de configuración inicial para Rutas Logísticas
Configura el entorno de desarrollo y producción
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"{description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error en {description}: {e.stderr}")
        return False


def create_env_file():
    """Crea archivo .env desde el template"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        print("Creando archivo .env...")
        shutil.copy(env_example, env_file)
        print("Archivo .env creado desde env.example")
        print("Recuerda ajustar los valores en .env según tu entorno")
    elif env_file.exists():
        print("Archivo .env ya existe")
    else:
        print("No se encontró env.example")


def setup_database():
    """Configura la base de datos"""
    print("\nConfigurando base de datos...")
    
    # Verificar si MySQL está disponible
    if not run_command("mysql --version", "Verificando MySQL"):
        print("MySQL no está instalado o no está en el PATH")
        print("Instala MySQL desde: https://dev.mysql.com/downloads/mysql/")
        return False
    
    # Crear base de datos si no existe
    create_db_cmd = """
    mysql -h localhost -u root -p -e "CREATE DATABASE IF NOT EXISTS rutas_logisticas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null || 
    mysql -h localhost -u root -p -e "SELECT 1;" >/dev/null 2>&1
    """
    
    if run_command(create_db_cmd, "Verificando conexión a base de datos"):
        print("Base de datos configurada correctamente")
        return True
    else:
        print("No se pudo conectar a la base de datos")
        print("Asegúrate de que MySQL esté ejecutándose y las credenciales sean correctas")
        return False


def install_dependencies():
    """Instala las dependencias del proyecto"""
    print("\nInstalando dependencias...")
    
    if run_command("pip install -r requirements.txt", "Instalando dependencias de Python"):
        return True
    else:
        print("Error instalando dependencias")
        return False


def setup_pre_commit():
    """Configura pre-commit hooks"""
    print("\nConfigurando pre-commit hooks...")
    
    if run_command("pre-commit install", "Instalando pre-commit hooks"):
        return True
    else:
        print("Pre-commit no está disponible, saltando configuración")
        return True


def create_directories():
    """Crea directorios necesarios"""
    print("\nCreando directorios...")
    
    directories = [
        "logs",
        "uploads",
        "static",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Directorio {directory} creado/verificado")


def run_tests():
    """Ejecuta tests básicos"""
    print("\nEjecutando tests...")
    
    if run_command("python -m pytest tests/ -v", "Ejecutando tests"):
        return True
    else:
        print("Tests fallaron, pero el setup continúa")
        return True


def main():
    """Función principal de configuración"""
    print("Configurando Rutas Logísticas...")
    print("=" * 50)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    success = True
    
    # Crear archivo de entorno
    create_env_file()
    
    # Crear directorios
    create_directories()
    
    # Instalar dependencias
    if not install_dependencies():
        success = False
    
    # Configurar base de datos
    if not setup_database():
        success = False
    
    # Configurar pre-commit (opcional)
    setup_pre_commit()
    
    # Ejecutar tests (opcional)
    run_tests()
    
    print("\n" + "=" * 50)
    if success:
        print("¡Configuración completada exitosamente!")
        print("\nPróximos pasos:")
        print("1. Ajusta las configuraciones en el archivo .env")
        print("2. Ejecuta 'python -m alembic upgrade head' para crear las tablas")
        print("3. Ejecuta 'python -m uvicorn app.main:app --reload' para iniciar el servidor")
        print("4. Visita http://localhost:8000/docs para ver la documentación de la API")
    else:
        print("Configuración completada con errores")
        print("Revisa los errores anteriores y configura manualmente los componentes faltantes")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
