from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from estacion.models import Estacion
from estacion.serializers import EstacionSerializer
from viajes.models import Viaje
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer
from bicicletas.models import Bicicleta, CondicionBicicleta
from django.utils import timezone
# Create your views here.


class EstacionViewSet(viewsets.ModelViewSet):
    queryset = Estacion.objects.all()
    serializer_class = EstacionSerializer

    @action(detail=True, methods=['post'])
    def retirar_bicicleta(self, request, pk=None):
        estacion = self.get_object()
        dni = request.data.get('dni')
        try:
            usuario = Usuario.objects.get(dni=dni)
        except Usuario.DoesNotExist:
            return Response(data={"error": "Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

        viaje = usuario.viaje_en_curso()
        if viaje:
            bicicleta = viaje.bicicleta
            return Response(data={"error": f"El usuario ya tiene un viaje en curso, porfavor devolver {bicicleta} primero"}, status=status.HTTP_400_BAD_REQUEST)

        bicicleta = estacion.bicicleta_disponible()
        if not bicicleta:
            return Response(data={'data': 'Esta Estacion no tiene bicicletas disponibles'}, status=status.HTTP_400_BAD_REQUEST)

        bicicleta.estacion = None
        bicicleta.save()
        Viaje.objects.create(bicicleta=bicicleta,
                             usuario=usuario, estado_inicial=bicicleta.estado)
        return Response(data={'data': f"Ya puede retirar la {bicicleta}"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def devolver_bicicleta(self, request, pk=None):
        estacion = self.get_object()
        dni = request.data.get('dni')
        descripcion = request.data.get('descripcion')
        estado = request.data.get('estado')

        try:
            usuario = Usuario.objects.get(dni=dni)
        except Usuario.DoesNotExist:
            return Response(data={"error": "Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

        viaje = usuario.viaje_en_curso()
        if viaje is None:
            return Response(data={'error': 'El usuario no tiene ningun viaje en curso'}, status=status.HTTP_400_BAD_REQUEST)

        if not estacion.espacios_disponibles():
            estacion_cercana = estacion.sugerir_estacion_cercana()
            if estacion_cercana:
                return Response(data={'data': f'Esta estacion se encuentra sin espacios disponibles, referirse a {estacion_cercana}'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            condicion = CondicionBicicleta[estado]
        except KeyError:
            return Response(data={'error': f"Estado Invalido: {estado}"},
                            status=status.HTTP_400_BAD_REQUEST)

        bicicleta = viaje.bicicleta
        bicicleta.estado = condicion.name
        bicicleta.estacion = estacion
        bicicleta.save()

        viaje.horario_llegada = timezone.now()
        viaje.estado_final = condicion.name
        viaje.save()

        multa = estacion.chequear_condicion(
            descripcion=descripcion, viaje=viaje)
        texto = ''
        if multa:
            texto += f"Se informa que se le ha agregado una multa debido ha que {multa.descripcion}"
        return Response(data={'data': f"El viaje se ha completado con exito, el total a pagar es {viaje.calcular_costo()}.{texto}"})
