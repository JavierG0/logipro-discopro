#!/bin/bash

# Script de utilidades para Discopro Django

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_color() {
    color=$1
    message=$2
    echo -e "${color}${message}${NC}"
}

# Función de ayuda
show_help() {
    echo "Uso: ./scripts.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  install         - Instalar dependencias"
    echo "  setup          - Configuración inicial (migraciones, superuser)"
    echo "  migrate        - Ejecutar migraciones"
    echo "  makemigrations - Crear archivos de migración"
    echo "  runserver      - Ejecutar servidor de desarrollo"
    echo "  test           - Ejecutar pruebas"
    echo "  seed           - Cargar datos iniciales"
    echo "  clean          - Limpiar archivos temporales"
    echo "  docker-build   - Construir imagen Docker"
    echo "  docker-up      - Iniciar contenedores Docker"
    echo "  docker-down    - Detener contenedores Docker"
    echo "  help           - Mostrar esta ayuda"
}

# Instalación de dependencias
install() {
    print_color "$YELLOW" "Instalando dependencias..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_color "$GREEN" "✓ Dependencias instaladas"
}

# Setup inicial
setup() {
    print_color "$YELLOW" "Ejecutando setup inicial..."
    
    # Crear .env si no existe
    if [ ! -f .env ]; then
        print_color "$YELLOW" "Creando archivo .env..."
        cp .env.example .env
        print_color "$YELLOW" "⚠ Por favor, edita .env con tus credenciales de MariaDB"
    fi
    
    # Migraciones
    print_color "$YELLOW" "Ejecutando migraciones..."
    python manage.py makemigrations
    python manage.py migrate
    
    # Crear superusuario
    print_color "$YELLOW" "Creando superusuario..."
    python manage.py createsuperuser
    
    print_color "$GREEN" "✓ Setup completado"
}

# Ejecutar migraciones
migrate() {
    print_color "$YELLOW" "Ejecutando migraciones..."
    python manage.py migrate
    print_color "$GREEN" "✓ Migraciones aplicadas"
}

# Crear migraciones
makemigrations() {
    print_color "$YELLOW" "Creando archivos de migración..."
    python manage.py makemigrations
    print_color "$GREEN" "✓ Migraciones creadas"
}

# Ejecutar servidor
runserver() {
    print_color "$YELLOW" "Iniciando servidor..."
    print_color "$GREEN" "Accede a http://localhost:8000"
    python manage.py runserver
}

# Ejecutar pruebas
test() {
    print_color "$YELLOW" "Ejecutando pruebas..."
    python manage.py test
    print_color "$GREEN" "✓ Pruebas completadas"
}

# Cargar datos iniciales
seed() {
    print_color "$YELLOW" "Cargando datos iniciales..."
    python manage.py shell < seed.py
    print_color "$GREEN" "✓ Datos cargados"
}

# Limpiar archivos temporales
clean() {
    print_color "$YELLOW" "Limpiando archivos temporales..."
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name ".coverage" -delete
    rm -rf htmlcov/
    print_color "$GREEN" "✓ Limpieza completada"
}

# Docker build
docker_build() {
    print_color "$YELLOW" "Construyendo imagen Docker..."
    docker-compose build
    print_color "$GREEN" "✓ Imagen construida"
}

# Docker up
docker_up() {
    print_color "$YELLOW" "Iniciando contenedores..."
    docker-compose up -d
    print_color "$GREEN" "✓ Contenedores iniciados"
    print_color "$YELLOW" "Accede a http://localhost"
}

# Docker down
docker_down() {
    print_color "$YELLOW" "Deteniendo contenedores..."
    docker-compose down
    print_color "$GREEN" "✓ Contenedores detenidos"
}

# Main
case "${1:-help}" in
    install)
        install
        ;;
    setup)
        setup
        ;;
    migrate)
        migrate
        ;;
    makemigrations)
        makemigrations
        ;;
    runserver)
        runserver
        ;;
    test)
        test
        ;;
    seed)
        seed
        ;;
    clean)
        clean
        ;;
    docker-build)
        docker_build
        ;;
    docker-up)
        docker_up
        ;;
    docker-down)
        docker_down
        ;;
    help)
        show_help
        ;;
    *)
        print_color "$RED" "Comando desconocido: $1"
        show_help
        exit 1
        ;;
esac
