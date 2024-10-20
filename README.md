# Gestión de Registros - Backend en Flask

## Descripción

Este proyecto es una aplicación backend desarrollada en Flask que permite:

-   Subir archivos CSV o TXT con registros.
-   Buscar registros en una base de datos relacional por ID.
-   Validar los archivos y los registros según ciertos criterios (como fechas y correos electrónicos).

## Tecnologías Utilizadas

-   Python 3.13.0
-   Flask
-   Flask-SQLAlchemy
-   Marshmallow (para la validación de datos)

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

-   Python 3.13.0
-   pip (para gestionar las dependencias)

## Instalación

1. Clona este repositorio:

    git clone https://github.com/DFrausto97/prueba-t-cnica.git

2. Navega al directorio del proyecto:

    cd prueba-t-cnica

3. Crea y activa un entorno virtual (opcional pero recomendado):

    python -m venv venv
    source venv/bin/activate # En Windows: venv\Scripts\activate

4. Instala las dependencias:

    pip install -r requirements.txt

5. Ejecuta la aplicación:

    python app.py

### 6. Uso de la Aplicación

Instrucciones sobre cómo utilizar la aplicación una vez configurada.

## Uso

### Subir un archivo

1. Abre Postman y crea una nueva petición:
   Haz clic en "New" y selecciona "Request".
2. Configura el método y URL:
   Selecciona el método HTTP adecuado, como POST
   Ingresa la URL que te muestra al correr la aplicación y el endpoint, por ejemplo: http://localhost:5000/upload
3. Añade el archivo a la petición:
   Ve a la pestaña "Body".
   Selecciona "form-data".
   Añade un nuevo campo de tipo "file".
   Ingresa el nombre del campo (por ejemplo, file) y selecciona el archivo que deseas subir desde tu sistema.
4. Configura los Headers (si es necesario):
   Ve a la pestaña "Headers".
   Asegúrate de tener el header Content-Type configurado como multipart/form-data. A veces, Postman lo hace automáticamente.
5. Envía la petición:
   Haz clic en "Send".
6. Revisa la respuesta:
   Observa la respuesta en la parte inferior de Postman para asegurarte de que la carga fue exitosa.

### Buscar un registro por ID

1. Abre Postman y crea una nueva petición:
   Haz clic en "New" y selecciona "Request".
2. Configura el método y URL:
   Selecciona el método HTTP adecuado, como GET
   Ingresa la URL que te muestra al correr la aplicación y el endpoint, seguido del id que deseas obtener, por ejemplo: http://localhost:5000/registros/1
3. Envía la petición:
   Haz clic en "Send".
4. Revisa la respuesta:
   Observa la respuesta en la parte inferior de Postman.
