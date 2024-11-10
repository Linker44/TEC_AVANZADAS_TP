import pytest

pytestmark = pytest.mark.django_db


class TestUsuario:

    def test_viaje_en_curso(self, viaje_curso):
        usuario = viaje_curso.usuario
        assert usuario.viaje_en_curso().id == viaje_curso.id
