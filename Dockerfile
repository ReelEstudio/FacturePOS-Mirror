# 1. Base de Python moderna y ligera
FROM python:3.12-slim

# 2. Evita archivos temporales y asegura logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Instalación de librerías de sistema (Indispensables para WeasyPrint y Timezones)
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

# 4. Carpeta de trabajo
WORKDIR /app

# 5. Instalación de dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar el código del proyecto
COPY . .

# 7. Ejecutar migraciones y arrancar Gunicorn
# El 'migrate' crea las tablas en la base de datos de Railway automáticamente
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:${PORT:-8000} config.wsgi:application"]