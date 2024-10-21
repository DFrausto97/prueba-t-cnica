# Usar una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requerimientos
COPY ./requeriments.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r ./requeriments.txt

# Copiar todo el código en el contenedor
COPY . .

# Exponer el puerto en el que Flask correrá
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
