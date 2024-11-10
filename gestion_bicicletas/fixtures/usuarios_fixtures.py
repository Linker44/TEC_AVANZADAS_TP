import pytest
from usuarios.models import Usuario


@pytest.fixture
def usuario():
    return Usuario.objects.create(nombre="badminton", apellido="bear", dni="12345678")
