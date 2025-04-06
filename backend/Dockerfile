FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Copiar solo los archivos de configuración de Poetry
COPY pyproject.toml poetry.lock* /app/

# Instalar dependencias a través de Poetry
RUN poetry install --no-interaction --no-ansi

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto que utilizará la aplicación
EXPOSE 8000

# Comandos para iniciar la aplicación (ajusta según tu framework)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]