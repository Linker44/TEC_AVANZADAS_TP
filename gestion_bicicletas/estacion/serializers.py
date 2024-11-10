from rest_framework import serializers
from estacion.models import Estacion


class EstacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estacion
        fields = '__all__'
