# Usar imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=America/Bogota

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

# Copiar proyecto
COPY . /app/

# Crear directorios necesarios
RUN mkdir -p /app/logs /app/static /app/media

# Dar permisos
RUN chmod +x /app/manage.py

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput --clear || true

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["gunicorn", "--config", "gunicorn_config.py", "discopro.wsgi:application"]
