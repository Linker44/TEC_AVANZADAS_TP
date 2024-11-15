# Generated by Django 5.1.3 on 2024-11-10 18:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("estacion", "0001_initial"),
        ("viajes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="multa",
            name="viaje",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="multa",
                to="viajes.viaje",
            ),
        ),
    ]
