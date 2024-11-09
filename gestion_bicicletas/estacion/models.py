from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import math
from bicicletas.estados import CondicionBicicleta
from datetime import timedelta
# Create your models here.


class Multa(models.Model):
    costo = models.FloatField()
    descripcion = models.TextField()
    viaje = models.OneToOneField(
        "viajes.Viaje", on_delete=models.CASCADE, related_name="multa")


class Ubicacion(models.Model):
    name = models.CharField(max_length=150)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class Estacion(models.Model):
    capacidad = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    posicion = models.OneToOneField(Ubicacion, on_delete=models.CASCADE)

    def bicicleta_disponible(self):
        return self.bicicletas.all().first()

    def espacios_disponibles(self):
        return (self.capacidad - len(self.bicicletas.all())) > 0

    def _distancia_hasta(self, otra_estacion):
        x_diff = self.location.x - otra_estacion.location.x
        y_diff = self.location.y - otra_estacion.location.y
        return math.sqrt(x_diff**2 + y_diff**2)

    def sugerir_estacion_cercana(self):
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

    def chequear_condicion(self, bicicleta, descripcion, viaje):
        costo = 0

        if bicicleta.estado in [CondicionBicicleta.MALO, CondicionBicicleta.ROTA]:

            if bicicleta.estado == CondicionBicicleta.MALO:
                costo += 100.0

            if bicicleta.estado == CondicionBicicleta.ROTA:
                costo += 300.0

        if viaje.horario_llegada and viaje.horario_partida:
            duracion_viaje = viaje.horario_llegada - viaje.horario_partida

            if duracion_viaje > timedelta(hours=2):
                costo += 30

        if costo == 0:
            return None

        return Multa.objects.create(costo=costo, descripcion=descripcion, viaje=viaje)
