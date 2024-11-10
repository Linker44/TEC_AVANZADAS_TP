from django.db import models
from bicicletas.estados import CondicionBicicleta


# Create your models here.


class Viaje(models.Model):
    estado_inicial = models.CharField(
        max_length=20,
        choices=[(state.name, state.value) for state in CondicionBicicleta]
    )
    estado_final = models.CharField(
        max_length=20,
        choices=[(state.name, state.value) for state in CondicionBicicleta],
        null=True,
        blank=True
    )
    horario_partida = models.DateTimeField(auto_now_add=True)
    horario_llegada = models.DateTimeField(null=True, blank=True)
    costo = models.FloatField(default=0.0)
    usuario = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.CASCADE, related_name="viajes")
    bicicleta = models.ForeignKey(
        "bicicletas.Bicicleta", on_delete=models.SET_NULL, null=True, related_name="viajes")

    def calcular_costo(self):
        costo = 15.0
        multa = getattr(self, 'multa', None)
        if multa:
            costo += multa.costo
        return costo

    def __str__(self):
        return f"Viaje N{self.id}"
