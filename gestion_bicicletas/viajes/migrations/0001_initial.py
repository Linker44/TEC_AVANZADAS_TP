# Generated by Django 5.1.3 on 2024-11-10 18:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("bicicletas", "0002_initial"),
        ("usuarios", "0002_alter_usuario_dni"),
    ]

    operations = [
        migrations.CreateModel(
            name="Viaje",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "estado_inicial",
                    models.CharField(
                        choices=[
                            ("EXCELENTE", "Excelente"),
                            ("BUENO", "Bueno"),
                            ("MALO", "Malo"),
                            ("ROTA", "Rota"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "estado_final",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("EXCELENTE", "Excelente"),
                            ("BUENO", "Bueno"),
                            ("MALO", "Malo"),
                            ("ROTA", "Rota"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("horario_partida", models.DateTimeField(auto_now_add=True)),
                ("horario_llegada", models.DateTimeField(blank=True, null=True)),
                ("costo", models.FloatField(default=0.0)),
                (
                    "bicicleta",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="viajes",
                        to="bicicletas.bicicleta",
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="viajes",
                        to="usuarios.usuario",
                    ),
                ),
            ],
        ),
    ]
