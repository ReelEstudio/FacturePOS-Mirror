# Usamos una base de Python moderna y ligera
FROM python:3.12-slim

# Instalamos las librerías de sistema que WeasyPrint exige
# Estas son las mismas que instalarías en un Droplet de DigitalOcean
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalamos dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos tu código
COPY . .

# Comando de arranque
# NOTA: Cambia 'config.wsgi' por el nombre de tu carpeta de proyecto si es distinto
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "config.wsgi:application"]