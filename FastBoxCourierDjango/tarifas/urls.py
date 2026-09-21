from django.urls import path
from django.views.generic import RedirectView

from .views import (
    TarifaCreateView,
    TarifaDeleteView,
    TarifaDetailView,
    TarifaListView,
    TarifaUpdateView,
)


app_name = "tarifas"


urlpatterns = [
    path(
        "",
        RedirectView.as_view(
            pattern_name="tarifas:tarifa_lista",
            permanent=False,
        ),
        name="inicio",
    ),

    path(
        "tarifas/",
        TarifaListView.as_view(),
        name="tarifa_lista",
    ),

    path(
        "tarifas/nueva/",
        TarifaCreateView.as_view(),
        name="tarifa_crear",
    ),

    path(
        "tarifas/<int:pk>/",
        TarifaDetailView.as_view(),
        name="tarifa_detalle",
    ),

    path(
        "tarifas/<int:pk>/editar/",
        TarifaUpdateView.as_view(),
        name="tarifa_editar",
    ),

    path(
        "tarifas/<int:pk>/eliminar/",
        TarifaDeleteView.as_view(),
        name="tarifa_eliminar",
    ),
]