import pytest
import pytest
from bicicletas.estados import CondicionBicicleta
from usuarios.models import Usuario
from bicicletas.models import Bicicleta
from viajes.models import Viaje
from estacion.models import Ubicacion
from random import randint


@pytest.fixture
def ubicacion1():
    x = randint(0, 10)
    y = randint(0, 10)
    ubicacion = Ubicacion.objects.create(x=x, y=y, name="Constitucion 2269")
    yield ubicacion
    ubicacion.delete()


@pytest.fixture
def ubicacion2():
    ubicacion = Ubicacion.objects.create(
        x=randint(0, 10), y=randint(0, 10), name="Cordoba 458")
    yield ubicacion
    ubicacion.delete()
