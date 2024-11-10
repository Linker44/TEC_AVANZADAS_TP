from rest_framework import serializers
from bicicletas.models import Bicicleta


class BicicletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicicleta
        fields = '__all__'
