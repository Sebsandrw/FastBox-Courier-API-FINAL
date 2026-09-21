from django.urls import path
from django.views.generic import RedirectView

from .views import (
    ClienteCreateView,
    ClienteDeleteView,
    ClienteDetailView,
    ClienteListView,
    ClienteUpdateView,
)


app_name = "clientes"


urlpatterns = [
    path(
        "",
        RedirectView.as_view(
            pattern_name="clientes:cliente_lista",
            permanent=False,
        ),
        name="inicio",
    ),

    path(
        "clientes/",
        ClienteListView.as_view(),
        name="cliente_lista",
    ),

    path(
        "clientes/nuevo/",
        ClienteCreateView.as_view(),
        name="cliente_crear",
    ),

    path(
        "clientes/<int:pk>/",
        ClienteDetailView.as_view(),
        name="cliente_detalle",
    ),

    path(
        "clientes/<int:pk>/editar/",
        ClienteUpdateView.as_view(),
        name="cliente_editar",
    ),

    path(
        "clientes/<int:pk>/eliminar/",
        ClienteDeleteView.as_view(),
        name="cliente_eliminar",
    ),
]