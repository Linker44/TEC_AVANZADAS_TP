import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from estacion.models import Estacion, Multa
from estacion.views import EstacionViewSet
from usuarios.models import Usuario
from bicicletas.models import Bicicleta, CondicionBicicleta
from viajes.models import Viaje

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def bicicleta(estacion):
    return Bicicleta.objects.create(estacion=estacion)


@pytest.fixture
def viaje_curso(usuario, bicicleta):
    return Viaje.objects.create(usuario=usuario, bicicleta=bicicleta, estado_inicial="EXCELENTE")


@pytest.fixture
def bicicleta_suelta():
    return Bicicleta.objects.create()


def test_retirar_bicicleta_success(api_client, usuario, estacion, bicicleta):
    url = f"/estaciones/{estacion.id}/retirar_bicicleta/"
    response = api_client.post(
        url, data={'dni': usuario.dni})

    assert response.status_code == status.HTTP_201_CREATED
    assert f"Ya puede retirar la {bicicleta}" in response.data['data']
    assert Bicicleta.objects.filter(estacion=None).exists()


def test_retirar_bicicleta_fail_usuario(api_client, estacion, bicicleta):
    url = f"/estaciones/{estacion.id}/retirar_bicicleta/"
    response = api_client.post(
        url, data={'dni': 12345678})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Usuario no encontrado" in response.data['error']


def test_retirar_bicicleta_viaje_en_curso(api_client, usuario, estacion, bicicleta, viaje_curso):
    url = f"/estaciones/{estacion.id}/retirar_bicicleta/"
    response = api_client.post(
        url, data={'dni': usuario.dni})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert f"El usuario ya tiene un viaje en curso, porfavor devolver {bicicleta} primero" in response.data[
        'error']


def test_retirar_bicicleta_fail_bicicletas_disponibles(api_client, usuario, estacion):
    url = f"/estaciones/{estacion.id}/retirar_bicicleta/"
    response = api_client.post(
        url, data={'dni': usuario.dni})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert f"Esta Estacion no tiene bicicletas disponibles" in response.data[
        'error']


def test_retirar_bicicleta_fail_bicicletas_disponibles(api_client, usuario, estacion):
    url = f"/estaciones/{estacion.id}/retirar_bicicleta/"
    response = api_client.post(
        url, data={'dni': usuario.dni})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert f"Esta Estacion no tiene bicicletas disponibles" in response.data[
        'error']


def test_devolver_bicicleta(api_client, usuario, estacion, bicicleta, viaje_curso):
    url = f"/estaciones/{estacion.id}/devolver_bicicleta/"
    data = {
        "dni": usuario.dni,
        "descripcion": "La bicicleta se encuentra en buen estado",
        "bicicleta": bicicleta.id,
        "estado": "EXCELENTE"
    }
    response = api_client.post(
        url, data=data)

    assert response.status_code == status.HTTP_200_OK
    viaje = Viaje.objects.filter(id=viaje_curso.id).first()
    multa = Multa.objects.filter(viaje=viaje).first()
    assert viaje.estado_final == "EXCELENTE"
    assert viaje.horario_llegada is not None
    assert multa is None


def test_devolver_bicicleta_fail_usuario(api_client, estacion, bicicleta):
    url = f"/estaciones/{estacion.id}/devolver_bicicleta/"
    data = {
        "dni": 4422321,
        "descripcion": "La bicicleta se encuentra en buen estado",
        "bicicleta": bicicleta.id,
        "estado": "EXCELENTE"
    }
    response = api_client.post(
        url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Usuario no encontrado" in response.data['error']


def test_devolver_bicicleta_fail_viaje_en_curso(api_client, usuario, estacion, bicicleta):
    url = f"/estaciones/{estacion.id}/devolver_bicicleta/"
    data = {
        "dni": usuario.dni,
        "descripcion": "La bicicleta se encuentra en buen estado",
        "bicicleta": bicicleta.id,
        "estado": "EXCELENTE"
    }
    response = api_client.post(
        url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "El usuario no tiene ningun viaje en curso" in response.data['error']


def test_devolver_bicicleta_fail_bicicleta_no_existe(api_client, usuario, estacion, bicicleta, viaje_curso):
    url = f"/estaciones/{estacion.id}/devolver_bicicleta/"
    data = {
        "dni": usuario.dni,
        "descripcion": "La bicicleta se encuentra en buen estado",
        "bicicleta": 233,
        "estado": "EXCELENTE"
    }
    response = api_client.post(
        url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "La bicicleta no pertenece al sistema" in response.data['error']


def test_devolver_bicicleta_fail_bicicleta_no_pertenece_a_usuario(api_client, usuario, bicicleta, estacion, viaje_curso, estacion_llena):
    url = f"/estaciones/{estacion_llena.id}/devolver_bicicleta/"
    data = {
        "dni": usuario.dni,
        "descripcion": "La bicicleta se encuentra en buen estado",
        "bicicleta": bicicleta.id,
        "estado": "EXCELENTE"
    }
    response = api_client.post(
        url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert f"Esta estacion se encuentra sin espacios disponibles, referirse a {estacion}" in response.data[
        'error']
