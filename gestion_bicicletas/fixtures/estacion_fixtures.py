import pytest
import pytest
from bicicletas.estados import CondicionBicicleta
from usuarios.models import Usuario
from bicicletas.models import Bicicleta
from viajes.models import Viaje
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
