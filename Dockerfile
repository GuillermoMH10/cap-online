# Imagen base
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Carpeta de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Actualizar pip
RUN pip install --upgrade pip

# Instalar dependencias
RUN pip install -r requirements.txt

# Copiar el proyecto
COPY . .

# Puerto usado por Render (el valor real lo proporciona la variable PORT)
EXPOSE 10000

# Ejecutar Gunicorn en el puerto asignado por Render
CMD ["sh", "-c", "gunicorn cap_online.wsgi:application --bind 0.0.0.0:${PORT:-10000}"]