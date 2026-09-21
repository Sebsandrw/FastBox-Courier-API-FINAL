from django.contrib.auth import authenticate
from django.db.models.deletion import ProtectedError
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from bitacora.models import Bitacora
from clientes.models import Cliente
from envios.models import MovimientoEnvio, Paquete
from tarifas.models import Tarifa

from .serializers import (
    BitacoraSerializer,
    ClienteSerializer,
    MovimientoEnvioSerializer,
    PaqueteSerializer,
    TarifaSerializer,
)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def login_api(request):
    """Valida usuarios de Django para la aplicacion movil."""

    if request.method == "GET":
        return Response({
            "servicio": "Autenticacion FastBox Courier",
            "metodo": "POST",
            "campos": ["username", "password"],
        })

    username = str(request.data.get("username", "")).strip()
    password = str(request.data.get("password", ""))

    if not username or not password:
        return Response(
            {"detail": "Ingrese usuario y contrasena."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    usuario = authenticate(
        request=request,
        username=username,
        password=password,
    )

    if usuario is None or not usuario.is_active:
        return Response(
            {"detail": "Usuario o contrasena incorrectos."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    nombre = usuario.get_full_name().strip() or usuario.username
    rol = "Administrador" if usuario.is_superuser else "Operador"

    return Response({
        "ok": True,
        "usuario": {
            "id": usuario.id,
            "usuario": usuario.username,
            "nombre": nombre,
            "correo": usuario.email,
            "rol": rol,
        },
    })


class ProtectedDestroyMixin:
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)

        except ProtectedError:
            return Response(
                {
                    "detalle": "No se puede eliminar este registro porque tiene información relacionada."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ClienteViewSet(ProtectedDestroyMixin, viewsets.ModelViewSet):
    serializer_class = ClienteSerializer

    def get_queryset(self):
        queryset = Cliente.objects.all().order_by("apellidos", "nombres")

        buscar = self.request.query_params.get("buscar")
        estado = self.request.query_params.get("estado")

        if buscar:
            queryset = queryset.filter(nombres__icontains=buscar) | queryset.filter(
                apellidos__icontains=buscar
            ) | queryset.filter(casillero__icontains=buscar)

        if estado in ["true", "false"]:
            queryset = queryset.filter(estado=(estado == "true"))

        return queryset


class TarifaViewSet(ProtectedDestroyMixin, viewsets.ModelViewSet):
    serializer_class = TarifaSerializer

    def get_queryset(self):
        queryset = Tarifa.objects.all().order_by("categoria")

        categoria = self.request.query_params.get("categoria")
        estado = self.request.query_params.get("estado")

        if categoria:
            queryset = queryset.filter(categoria=categoria)

        if estado in ["true", "false"]:
            queryset = queryset.filter(estado=(estado == "true"))

        return queryset


class PaqueteViewSet(ProtectedDestroyMixin, viewsets.ModelViewSet):
    serializer_class = PaqueteSerializer

    def get_queryset(self):
        queryset = (
            Paquete.objects
            .select_related("cliente", "tarifa")
            .order_by("-fecha_registro")
        )

        buscar = self.request.query_params.get("buscar")
        estado = self.request.query_params.get("estado")

        if buscar:
            queryset = queryset.filter(guia_fastbox__icontains=buscar) | queryset.filter(
                tracking_original__icontains=buscar
            ) | queryset.filter(descripcion__icontains=buscar)

        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset


class MovimientoEnvioViewSet(ProtectedDestroyMixin, viewsets.ModelViewSet):
    serializer_class = MovimientoEnvioSerializer

    def get_queryset(self):
        return (
            MovimientoEnvio.objects
            .select_related("paquete")
            .order_by("-fecha_hora")
        )

    def perform_create(self, serializer):
        movimiento = serializer.save()

        paquete = movimiento.paquete
        paquete.estado = movimiento.estado
        paquete.save()

    def perform_update(self, serializer):
        movimiento = serializer.save()

        paquete = movimiento.paquete
        paquete.estado = movimiento.estado
        paquete.save()


class BitacoraViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BitacoraSerializer

    def get_queryset(self):
        return Bitacora.objects.all().order_by("-fecha_hora")