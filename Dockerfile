# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos y el script al directorio de trabajo
COPY requirements.txt .
COPY comprobar_stock.py .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el script cuando el contenedor se inicie
CMD ["python3", "-u", "comprobar_stock.py"]
