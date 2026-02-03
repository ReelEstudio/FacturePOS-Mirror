# Usamos Python 3.12 Slim (Debian Trixie/Bookworm)
FROM python:3.12-slim

# Evitamos que Python genere archivos .pyc y que el buffer se congele
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalamos las librerías de sistema necesarias para WeasyPrint
# Nota: libgdk-pixbuf-2.0-0 lleva el guion extra que pedía el error anterior
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos e instalamos dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Railway inyecta la variable $PORT automáticamente. 
# Usamos 0.0.0.0 para que sea accesible externamente.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8080} config.wsgi:application"]