import pytest
from bicicletas.models import Bicicleta, CondicionBicicleta


@pytest.fixture
def bicicleta():
    bicicleta = Bicicleta.objects.create(
        estado=CondicionBicicleta.EXCELENTE.name)
    yield bicicleta
    bicicleta.delete()


@pytest.fixture
def bicicleta_malo():
    bicicleta = Bicicleta.objects.create(
        estado=CondicionBicicleta.MALO.name)
    yield bicicleta
    bicicleta.delete()


@pytest.fixture
def bicicleta_rota():
    bicicleta = Bicicleta.objects.create(
        estado=CondicionBicicleta.ROTA.name)
    yield bicicleta
    bicicleta.delete()
