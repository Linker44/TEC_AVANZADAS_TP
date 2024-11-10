import pytest
import pytest
from bicicletas.estados import CondicionBicicleta
from usuarios.models import Usuario
from viajes.models import Viaje


@pytest.fixture
def viaje(usuario, bicicleta):
    viaje = Viaje.objects.create(
        estado_inicial=CondicionBicicleta.EXCELENTE.name,
        usuario=usuario,
        bicicleta=bicicleta,
    )
    yield viaje
    viaje.delete()


@pytest.fixture
def viaje_curso(usuario, bicicleta):
    return Viaje.objects.create(usuario=usuario, bicicleta=bicicleta, estado_inicial="EXCELENTE")
