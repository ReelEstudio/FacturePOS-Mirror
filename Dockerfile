# 1. Usamos la imagen base de Python 3.12 (Debian Trixie/Bookworm)
FROM python:3.12-slim

# 2. Variables de entorno para optimizar Python en Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Instalación de dependencias del sistema operativo
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    tzdata \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 5. Instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar todo el código de tu proyecto al contenedor
COPY . .

# 7. Comando para arrancar la aplicación
# IMPORTANTE: Hemos añadido 'python manage.py migrate' antes de arrancar Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:${PORT:-8000} config.wsgi:application"]