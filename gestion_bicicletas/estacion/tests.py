import pytest
from estacion.models import Estacion, Ubicacion
from django.core.exceptions import ValidationError
pytestmark = pytest.mark.django_db


class TestEstacion:

    def test_capacidad_error(self, ubicacion1):
        estacion = Estacion(posicion=ubicacion1, capacidad=21)
        with pytest.raises(ValidationError):
            estacion.full_clean()

    def test_bicicleta_disponible(self, ubicacion1, bicicleta):
        estacion = Estacion.objects.create(posicion=ubicacion1, capacidad=5)
        bicicleta.estacion = estacion
        bicicleta.save()
        assert estacion.bicicleta_disponible() == bicicleta
        estacion.delete()

    def test_bicicleta_no_disponible(self, ubicacion1, bicicleta_rota):
        estacion = Estacion.objects.create(
            posicion=ubicacion1, capacidad=5)
        bicicleta_rota.estacion = estacion
        bicicleta_rota.save()
        assert estacion.bicicleta_disponible() is None
        estacion.delete()

    def test_espacios_disponibles_true(self, ubicacion1, bicicleta):
        estacion = Estacion.objects.create(posicion=ubicacion1, capacidad=5)
        bicicleta.estacion = estacion
        bicicleta.save()
        assert estacion.espacios_disponibles()
        estacion.delete()

    def test_espacios_disponibles_false(self, ubicacion1, bicicleta, bicicleta_malo):
        estacion = Estacion.objects.create(
            posicion=ubicacion1, capacidad=2)

        bicicleta.estacion = estacion
        bicicleta_malo.estacion = estacion

        bicicleta.save()
        bicicleta_malo.save()

        assert not estacion.espacios_disponibles()
        estacion.delete()

    def test_sugerir_estacion_cercana(self):
        ubicacion_1 = Ubicacion.objects.create(
            x=1, y=2, name="La paternal 229")
        ubicacion_2 = Ubicacion.objects.create(
            x=5, y=3, name="Francisco Diaz 23")
        ubicacion_3 = Ubicacion.objects.create(
            x=2, y=2, name="Coronel marcos 34")

        estacion_1 = Estacion.objects.create(
            id=1, posicion=ubicacion_1, capacidad=2)
        estacion_2 = Estacion.objects.create(
            id=2, posicion=ubicacion_2, capacidad=2)
        estacion_3 = Estacion.objects.create(
            id=3, posicion=ubicacion_3, capacidad=2)

        assert estacion_1.sugerir_estacion_cercana() == estacion_3

        estacion_1.delete()
        estacion_2.delete()
        estacion_3.delete()

    def test_sugerir_estacion_cercana_con_espacio_disponible(self, bicicleta, bicicleta_malo):
        ubicacion_1 = Ubicacion.objects.create(
            x=1, y=2, name="La paternal 229")
        ubicacion_2 = Ubicacion.objects.create(
            x=5, y=3, name="Francisco Diaz 23")
        ubicacion_3 = Ubicacion.objects.create(
            x=2, y=2, name="Coronel marcos 34")

        estacion_1 = Estacion.objects.create(
            id=1, posicion=ubicacion_1, capacidad=2)
        estacion_2 = Estacion.objects.create(
            id=2, posicion=ubicacion_2, capacidad=2)
        # es la estacion mas cercana pero no tiene espacio disponible
        estacion_3 = Estacion.objects.create(
            id=3, posicion=ubicacion_3, capacidad=2)
        bicicleta.estacion = estacion_3
        bicicleta_malo.estacion = estacion_3
        bicicleta.save()
        bicicleta_malo.save()

        assert estacion_1.sugerir_estacion_cercana() == estacion_2

        estacion_1.delete()
        estacion_2.delete()
        estacion_3.delete()

    def test_sugerir_estacion_cercana_none(self, bicicleta, bicicleta_malo):
        ubicacion_1 = Ubicacion.objects.create(
            x=1, y=2, name="La paternal 229")
        ubicacion_3 = Ubicacion.objects.create(
            x=2, y=2, name="Coronel marcos 34")

        estacion_1 = Estacion.objects.create(
            id=1, posicion=ubicacion_1, capacidad=2)
        # es la estacion mas cercana pero no tiene espacio disponible
        estacion_3 = Estacion.objects.create(
            id=3, posicion=ubicacion_3, capacidad=2)
        bicicleta.estacion = estacion_3
        bicicleta_malo.estacion = estacion_3
        bicicleta.save()
        bicicleta_malo.save()

        # no hay estaciones disponibles
        assert estacion_1.sugerir_estacion_cercana() is None

        estacion_1.delete()
        estacion_3.delete()

    def test_chequear_condicion(self, ubicacion1, bicicleta_rota, viaje):
        estacion = Estacion.objects.create(
            posicion=ubicacion1, capacidad=2)

        viaje.bicicleta = bicicleta_rota
        viaje.save()

        estacion.chequear_condicion(
            descripcion="Le falta el manubrio", viaje=viaje)

        multa = viaje.multa
        assert multa is not None
        assert multa.costo == 300.0
        assert multa.descripcion == "Le falta el manubrio"
        assert viaje.calcular_costo() == 315.0

        estacion.delete()
