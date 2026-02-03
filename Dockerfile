# Usamos la misma base
FROM python:3.12-slim

# Evita archivos temporales de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalamos las librerías con los nombres exactos para Debian Trixie/Bookworm
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

# Instalamos dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código
COPY . .

# Comando de arranque
# Asegúrate de que 'config.wsgi' coincide con el nombre de tu carpeta de proyecto
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "config.wsgi:application"]