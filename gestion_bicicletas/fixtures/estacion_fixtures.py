import pytest
import pytest
from estacion.models import Estacion
from bicicletas.models import Bicicleta
from random import randint


@pytest.fixture
def ubicacion1():
    x = randint(0, 10)
    y = randint(0, 10)
    return {"x": x, "y": y}


@pytest.fixture
def ubicacion2():
    x = randint(0, 10)
    y = randint(0, 10)
    return {"x": x, "y": y}


@pytest.fixture
def estacion():
    return Estacion.objects.create(name="Estacion 1", posicion={"x": 1, "y": 2}, capacidad=5)


@pytest.fixture
def estacion_llena():
    estacion = Estacion.objects.create(name="Estacion 1", posicion={
                                       "x": 1, "y": 3}, capacidad=1)
    Bicicleta.objects.create(estacion=estacion)
    return estacion
