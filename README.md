# TEC_AVANZADAS_TP

Trabajo Practico para la materia tecnicas avanzadas de programacion.

## REQUERIMIENTOS:

- Tener postgres instalado.
- Crear una base de datos llamada gestionbicicletas.
- Crear un usuario con SuperUser permissions llamado myuser.

## HOW TO RUN:

- crear un venv utilizando `python -m python venv ./env`.
- dentro del directorio gestion_bicicletas correr `python manage.py migrate`
- dentro del directorio gestion_bicicletas correr `python manage.py runserver`.
- si se desea popular la base de datos: dentro del directorio gestion_bicicletas correr `python setup.py`.
