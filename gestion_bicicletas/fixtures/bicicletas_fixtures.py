import pytest
from bicicletas.models import Bicicleta, CondicionBicicleta


@pytest.fixture
def bicicleta():
    return Bicicleta.objects.create(
        estado=CondicionBicicleta.EXCELENTE.name)


@pytest.fixture
def bicicleta_malo():
    return Bicicleta.objects.create(
        estado=CondicionBicicleta.MALO.name)


@pytest.fixture
def bicicleta_rota():
    return Bicicleta.objects.create(
        estado=CondicionBicicleta.ROTA.name)
