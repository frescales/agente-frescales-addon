FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copiar todos los archivos
COPY . /app

# 👇 Copiar explícitamente el archivo .env (por si COPY . no lo incluye)
COPY .env /app/.env

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Permisos para script de arranque
RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
