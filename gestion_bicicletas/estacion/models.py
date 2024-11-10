from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import math
from bicicletas.estados import CondicionBicicleta
from datetime import timedelta
from django.core.exceptions import ValidationError
# Create your models here.


class Multa(models.Model):
    costo = models.FloatField()
    descripcion = models.TextField()
    viaje = models.OneToOneField(
        "viajes.Viaje", on_delete=models.CASCADE, related_name="multa")


def validar_posicion(value):
    if not isinstance(value, dict):
        raise ValidationError("La posicion debe ser un diccionario")
    if "x" not in value or "y" not in value:
        raise ValidationError("La posicion debe contener los ejes 'x' y 'y'")
    if not isinstance(value["x"], int) or not isinstance(value["y"], int):
        raise ValidationError("'x' and 'y' deben ser integers.")


class Estacion(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    capacidad = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    posicion = models.JSONField(validators=[validar_posicion])

    def bicicleta_disponible(self):
        return self.bicicletas.all().exclude(estado=CondicionBicicleta.ROTA.name).first()

    def espacios_disponibles(self):
        return (self.capacidad - len(self.bicicletas.all())) > 0

    def _distancia_hasta(self, otra_estacion):
        x_diff = self.posicion["x"] - otra_estacion.posicion["x"]
        y_diff = self.posicion["y"] - otra_estacion.posicion["y"]
        return math.sqrt(x_diff**2 + y_diff**2)

    def sugerir_estacion_cercana(self):
        """Devuelve la estacion mas cercana que tenga espacios disponibles"""
        estaciones = Estacion.objects.exclude(id=self.id)
        estacion_cercana = None
        menor_distancia = float("inf")

        for estacion in [
            disponible for disponible in estaciones if disponible.espacios_disponibles()
        ]:
            distancia = self._distancia_hasta(estacion)
            if distancia < menor_distancia:
                estacion_cercana = estacion
                menor_distancia = distancia

        return estacion_cercana

    def chequear_condicion(self, descripcion, viaje):
        costo = 0
        bicicleta = viaje.bicicleta

        if bicicleta.estado in [CondicionBicicleta.MALO.name, CondicionBicicleta.ROTA.name]:

            if bicicleta.estado == CondicionBicicleta.MALO.name:
                costo += 100.0

            if bicicleta.estado == CondicionBicicleta.ROTA.name:
                costo += 300.0

        if viaje.horario_llegada and viaje.horario_partida:
            duracion_viaje = viaje.horario_llegada - viaje.horario_partida

            if duracion_viaje > timedelta(hours=2):
                costo += 30
                descripcion += ' La bicicleta no se ha entregado dentro del horario solicitado.'

        if costo == 0:
            return None

        return Multa.objects.create(costo=costo, descripcion=descripcion, viaje=viaje)

    def __str__(self):
        return f"Estacion {self.name}"
