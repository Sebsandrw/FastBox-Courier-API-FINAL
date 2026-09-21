from django.views.generic import ListView

from .models import Bitacora


class BitacoraListView(ListView):
    model = Bitacora
    template_name = "bitacora/bitacora_list.html"
    context_object_name = "registros"
    paginate_by = 15

    extra_context = {
        "titulo_pagina": "Bitácora del sistema",
    }

    def get_queryset(self):
        return Bitacora.objects.all().order_by("-fecha_hora")