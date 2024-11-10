from rest_framework import viewsets
from bicicletas.models import Bicicleta
from bicicletas.serializers import BicicletaSerializer
# Create your views here.


class BicicletaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bicicleta.objects.all()
    serializer_class = BicicletaSerializer
