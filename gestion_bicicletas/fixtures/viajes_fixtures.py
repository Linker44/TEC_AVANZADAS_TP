import pytest
import pytest
from bicicletas.estados import CondicionBicicleta
from usuarios.models import Usuario
from viajes.models import Viaje


@pytest.fixture
def usuario():
    usuario = Usuario.objects.create(
        nombre="test", apellido="user", dni="40243756")
    yield usuario
    usuario.delete()


@pytest.fixture
def viaje(usuario, bicicleta):
    viaje = Viaje.objects.create(
        estado_inicial=CondicionBicicleta.EXCELENTE.name,
        usuario=usuario,
        bicicleta=bicicleta,
    )
    yield viaje
    viaje.delete()
