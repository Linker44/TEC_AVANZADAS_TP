from django.db import models

# Create your models here.


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.IntegerField(unique=True)

    def viaje_en_curso(self):
        return self.viajes.order_by('-horario_partida').filter(horario_llegada=None).first()
