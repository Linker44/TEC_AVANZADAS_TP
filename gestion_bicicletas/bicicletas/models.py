from django.db import models
from bicicletas.estados import CondicionBicicleta

# Create your models here.


class Bicicleta(models.Model):
    estado = models.CharField(
        max_length=20,
        choices=[(state.name, state.value) for state in CondicionBicicleta],
        default=CondicionBicicleta.EXCELENTE.name,
    )
    estacion = models.ForeignKey(
        "estacion.Estacion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bicicletas",
    )

    def __str__(self):
        return f"Bicicleta {self.id}"
