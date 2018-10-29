## Setup

1. Generar entorno mediante virtualenv `virtualenv -p python3 env` o pyenv `pyenv env`.
1. Activar virtualenv/pyenv con `source ./env/bin/activate`.
1. Instalar las dependencias (debe hacerse corriendo en el env) con `(sudo) pip install -r requirements.txt`.
1. Ejecutar aplicación utilizando un webserver:
    * Utilizando flask `export FLASK_APP=app.py && flask run --host=0.0.0.0 --port=8000`.
    * Ejecutar aplicacion con gunicorn como webserver `gunicorn -w 4 -b 0.0.0.0:8000 app:app --log-level=debug`

## Para correr con Docker

1. Abrir una terminal en el directorio base del proyecto.
1. Construye la imagen de docker con los siguientes comandos:

    ```
    (sudo) docker-compose build
    (sudo) docker-compose up
    ```