
import os
import django
from django.db import transaction
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_bicicletas.settings')
os.environ.get('DJANGO_SETTINGS_MODULE')
django.setup()


def populate_db():
    from usuarios.models import Usuario
    from bicicletas.models import Bicicleta
    from estacion.models import Estacion

    estaciones = [
        {
            "name": "paternal 829",
            "posicion": {"x": 2, "y": 2},
            "capacidad": 5
        },
        {
            "name": "rivadavia 22",
            "posicion": {"x": 3, "y": 2},
            "capacidad": 5
        },
        {
            "name": "chespirito 200",
            "posicion": {"x": 3, "y": 5},
            "capacidad": 4
        },
        {
            "name": "monsenieur larumbe 43",
            "posicion": {"x": 6, "y": 2},
            "capacidad": 3
        }
    ]

    usuarios = [
        {"nombre": "roberto", "apellido": "perez", "dni": 4068229},
        {"nombre": "facundo", "apellido": "lopez", "dni": 4064332},
    ]

    try:
        with transaction.atomic():
            created_usuarios = []
            for usuario in usuarios:
                created_usuarios.append(Usuario.objects.create(**usuario))

            created_estaciones = []
            for estacion in estaciones:
                estacion_creada = Estacion.objects.create(**estacion)
                created_estaciones.append(estacion_creada)
                for _ in range(estacion_creada.capacidad - 1):
                    Bicicleta.objects.create(estacion=estacion_creada)

    except Exception as e:

        for estacion in created_estaciones:
            Bicicleta.objects.filter(estacion=estacion).delete()
            estacion.delete()

        for usuario in created_usuarios:
            usuario.delete()


if __name__ == "__main__":
    populate_db()
