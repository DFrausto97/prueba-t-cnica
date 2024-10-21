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
-   Pandas (para el procesamiento de archivos)
-   Docker
-   PostgreSQL

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

-   Python 3.13.0
-   Docker y Docker Compose (para ejecutar la aplicación en contenedores)
-   pip (para gestionar las dependencias si decides ejecutarlo sin Docker)

## Instalación

### Opción 1: Instalación con Docker

1. Clona este repositorio:

    git clone https://github.com/DFrausto97/prueba-t-cnica.git

2. Navega al directorio del proyecto:

    cd prueba-t-cnica

3. Asegúrate de que Docker esté instalado y funcionando en tu sistema.

4. Construye y levanta los contenedores (incluye PostgreSQL y la aplicación Flask):

    docker-compose up --build

    Esto descargará las imágenes necesarias, construirá los contenedores y levantará la aplicación Flask en conjunto con una base de datos PostgreSQL.

5. Crear las migraciones:

    docker-compose run web flask db init  
    docker-compose run web flask db migrate
    docker-compose run web flask db upgrade

6. Accede a la aplicación desde tu navegador o desde herramientas como Postman en la siguiente URL:

    http://localhost:5000

### Opción 2: Instalación Manual

1. Clona este repositorio:

    git clone https://github.com/DFrausto97/prueba-t-cnica.git

2. Navega al directorio del proyecto:

    cd prueba-t-cnica

3. Crea y activa un entorno virtual (opcional pero recomendado):

    python -m venv venv
    source venv/bin/activate # En Windows: venv\Scripts\activate

4. Instala las dependencias:

    pip install -r requirements.txt

5. Configura la base de datos PostgreSQL (debes tener PostgreSQL instalado en tu máquina o usar otro servidor remoto).

6. Ejecuta la aplicación:

    python app.py

### Uso de la Aplicación

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

## Pagina web

En tu navegador, ingresa a la URL que te da al correr la aplicación, por ejemplo: http://localhost:5000/ y te mostrara un template donde podrás subir archivos y buscar registros por id.

### Subir un archivo

1. Ve a la pestaña "Subir Archivo".
2. Selecciona un archivo CSV o TXT con los registros que deseas cargar.
3. Haz clic en "Subir" y verás los resultados en un mensaje de alerta.

### Buscar un registro por ID

1. Ve a la pestaña "Buscar por ID".
2. Ingresa el ID del registro que deseas buscar y haz clic en "Buscar".
3. Si el registro existe, los detalles del mismo aparecerán en un mensaje de alerta.
