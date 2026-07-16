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

# Puerto de Django
EXPOSE 8020

# Ejecutar Django
CMD ["python","manage.py","runserver","0.0.0.0:8020"]