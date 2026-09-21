from django.urls import path
from django.views.generic import RedirectView

from .views import (
    MovimientoEnvioCreateView,
    MovimientoEnvioDeleteView,
    MovimientoEnvioDetailView,
    MovimientoEnvioListView,
    MovimientoEnvioUpdateView,
    PaqueteCreateView,
    PaqueteDeleteView,
    PaqueteDetailView,
    PaqueteListView,
    PaqueteUpdateView,
)


app_name = "envios"


urlpatterns = [
    path(
        "",
        RedirectView.as_view(
            pattern_name="envios:paquete_lista",
            permanent=False,
        ),
        name="inicio",
    ),

    path(
        "paquetes/",
        PaqueteListView.as_view(),
        name="paquete_lista",
    ),

    path(
        "paquetes/nuevo/",
        PaqueteCreateView.as_view(),
        name="paquete_crear",
    ),

    path(
        "paquetes/<int:pk>/",
        PaqueteDetailView.as_view(),
        name="paquete_detalle",
    ),

    path(
        "paquetes/<int:pk>/editar/",
        PaqueteUpdateView.as_view(),
        name="paquete_editar",
    ),

    path(
        "paquetes/<int:pk>/eliminar/",
        PaqueteDeleteView.as_view(),
        name="paquete_eliminar",
    ),

    path(
        "movimientos/",
        MovimientoEnvioListView.as_view(),
        name="movimiento_lista",
    ),

    path(
        "movimientos/nuevo/",
        MovimientoEnvioCreateView.as_view(),
        name="movimiento_crear",
    ),

    path(
        "movimientos/<int:pk>/",
        MovimientoEnvioDetailView.as_view(),
        name="movimiento_detalle",
    ),

    path(
        "movimientos/<int:pk>/editar/",
        MovimientoEnvioUpdateView.as_view(),
        name="movimiento_editar",
    ),

    path(
        "movimientos/<int:pk>/eliminar/",
        MovimientoEnvioDeleteView.as_view(),
        name="movimiento_eliminar",
    ),
]