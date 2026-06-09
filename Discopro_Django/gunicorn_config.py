"""
Configuración de Gunicorn para producción.
Uso: gunicorn --config gunicorn_config.py discopro.wsgi
"""

import multiprocessing

# Número de workers (procesos)
workers = multiprocessing.cpu_count() * 2 + 1

# Tipo de worker
worker_class = "sync"

# Puerto a escuchar
bind = "127.0.0.1:8000"

# Archivo de log
accesslog = "logs/access.log"
errorlog = "logs/error.log"

# Nivel de logging
loglevel = "info"

# Máximo de conexiones
max_requests = 1000

# Timeout de workers
timeout = 30

# Mantener vivo
keepalive = 2

# Límite de tamaño de request
limit_request_fields = 100
limit_request_field_size = 8190

# Reloader
reload = False

# Preload app
preload_app = True

# Daemon mode
daemon = False

# PID file
pidfile = "gunicorn.pid"
