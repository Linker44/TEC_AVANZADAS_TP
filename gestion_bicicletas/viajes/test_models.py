import pytest
from bicicletas.estados import CondicionBicicleta
from estacion.models import Multa
# Create your tests here.
pytestmark = pytest.mark.django_db


class TestViaje:

    def test_viaje_creation(self, viaje):
        assert viaje.estado_inicial == CondicionBicicleta.EXCELENTE.name
        assert viaje.estado_final is None
        assert viaje.usuario.nombre == "badminton"
        assert viaje.bicicleta.estado == CondicionBicicleta.EXCELENTE.name

    def test_calcular_costo(self, viaje):
        # Sin multa el costo base es 15
        assert viaje.calcular_costo() == 15.0

        # Create a multa for the viaje
        Multa.objects.create(
            costo=5.0, descripcion="Test Multa", viaje=viaje)

        # Despues de aplicar la multa el costo deberia ser de 20
        assert viaje.calcular_costo() == 20.0

    def test_str_method(self, viaje):
        assert str(viaje) == f"Viaje N{viaje.id}"
