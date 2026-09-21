from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    BitacoraViewSet,
    ClienteViewSet,
    MovimientoEnvioViewSet,
    PaqueteViewSet,
    TarifaViewSet,
    login_api,
)


router = DefaultRouter()

router.register(
    r"clientes",
    ClienteViewSet,
    basename="cliente",
)

router.register(
    r"tarifas",
    TarifaViewSet,
    basename="tarifa",
)

router.register(
    r"paquetes",
    PaqueteViewSet,
    basename="paquete",
)

router.register(
    r"movimientos",
    MovimientoEnvioViewSet,
    basename="movimiento",
)

router.register(
    r"bitacora",
    BitacoraViewSet,
    basename="bitacora",
)


urlpatterns = [
    path("auth/login/", login_api, name="api_login"),
] + router.urls