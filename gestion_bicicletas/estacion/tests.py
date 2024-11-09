import pytest
from django.utils import timezone
from bicicletas.estados import CondicionBicicleta
from usuarios.models import Usuario
from bicicletas.models import Bicicleta
from viajes.models import Viaje
from estacion.models import Multa
# Create your tests here.
pytestmark = pytest.mark.django_db


@pytest.fixture
def usuario():
    """Fixture to create a test usuario."""
    usuario = Usuario.objects.create(
        nombre="test", apellido="user", dni="40243756")
    yield usuario
    usuario.delete()


@pytest.fixture
def bicicleta():
    """Fixture to create a test bicicleta."""
    bicicleta = Bicicleta.objects.create(
        estado=CondicionBicicleta.EXCELENTE.name)
    yield bicicleta
    bicicleta.delete()


@pytest.fixture
def viaje(usuario, bicicleta):
    """Fixture to create a test viaje."""
    viaje = Viaje.objects.create(
        estado_inicial=CondicionBicicleta.EXCELENTE.name,
        estado_final=CondicionBicicleta.EXCELENTE.name,
        usuario=usuario,
        bicicleta=bicicleta,
    )
    yield viaje
    viaje.delete()


class TestViaje:

    def test_viaje_creation(self, viaje, usuario, bicicleta):
        """Test that a Viaje instance is created properly."""
        assert viaje.estado_inicial == CondicionBicicleta.EXCELENTE.name
        assert viaje.estado_final == CondicionBicicleta.EXCELENTE.name
        assert viaje.usuario.nombre == "test"
        assert viaje.bicicleta.estado == CondicionBicicleta.EXCELENTE.name

    def test_calcular_costo(self, viaje):
        """Test the calcular_costo method of the Viaje model."""
        # No multa applied yet, so the cost should be 15.0
        assert viaje.calcular_costo() == 15.0

        # Create a multa for the viaje
        multa = Multa.objects.create(
            costo=5.0, descripcion="Test Multa", viaje=viaje)

        # After applying the multa, the cost should be 20.0
        assert viaje.calcular_costo() == 20.0

    def test_str_method(self, viaje):
        """Test the __str__ method of the Viaje model."""
        assert str(viaje) == f"Viaje N{viaje.id}"
