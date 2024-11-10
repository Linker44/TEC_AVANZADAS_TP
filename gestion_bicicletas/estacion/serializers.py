from rest_framework import serializers
from estacion.models import Estacion
from bicicletas.serializers import BicicletaSerializer


class EstacionSerializer(serializers.ModelSerializer):
    bicicletas = BicicletaSerializer(many=True, read_only=True)

    class Meta:
        model = Estacion
        fields = '__all__'
