from django.urls import path

from .views import BitacoraListView


app_name = "bitacora"


urlpatterns = [
    path(
        "",
        BitacoraListView.as_view(),
        name="bitacora_lista",
    ),
]