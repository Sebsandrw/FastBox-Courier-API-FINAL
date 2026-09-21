from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from bitacora.utils import registrar_bitacora

from .forms import TarifaForm
from .models import Tarifa


class TarifaListView(ListView):
    model = Tarifa
    template_name = "tarifas/tarifa_list.html"
    context_object_name = "tarifas"
    paginate_by = 10

    extra_context = {
        "titulo_pagina": "Tarifas",
    }


class TarifaCreateView(CreateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = "tarifas/tarifa_form.html"
    success_url = reverse_lazy("tarifas:tarifa_lista")

    extra_context = {
        "titulo_pagina": "Registrar tarifa",
        "texto_boton": "Guardar tarifa",
    }

    def form_valid(self, form):
        response = super().form_valid(form)

        registrar_bitacora(
            self.request,
            "Tarifa registrada",
            f"Se registró una tarifa para {self.object.get_categoria_display()}.",
            "Tarifas",
        )

        messages.success(
            self.request,
            "Tarifa registrada correctamente.",
        )

        return response


class TarifaDetailView(DetailView):
    model = Tarifa
    template_name = "tarifas/tarifa_detail.html"
    context_object_name = "tarifa"

    extra_context = {
        "titulo_pagina": "Detalle de tarifa",
    }


class TarifaUpdateView(UpdateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = "tarifas/tarifa_form.html"
    success_url = reverse_lazy("tarifas:tarifa_lista")

    extra_context = {
        "titulo_pagina": "Editar tarifa",
        "texto_boton": "Actualizar tarifa",
    }

    def form_valid(self, form):
        response = super().form_valid(form)

        registrar_bitacora(
            self.request,
            "Tarifa actualizada",
            f"Se actualizó la tarifa de {self.object.get_categoria_display()}.",
            "Tarifas",
        )

        messages.success(
            self.request,
            "Tarifa actualizada correctamente.",
        )

        return response


class TarifaDeleteView(DeleteView):
    model = Tarifa
    template_name = "tarifas/tarifa_confirm_delete.html"
    context_object_name = "tarifa"
    success_url = reverse_lazy("tarifas:tarifa_lista")

    extra_context = {
        "titulo_pagina": "Eliminar tarifa",
    }

    def form_valid(self, form):
        try:
            categoria = self.object.get_categoria_display()

            response = super().form_valid(form)

            registrar_bitacora(
                self.request,
                "Tarifa eliminada",
                f"Se eliminó la tarifa de {categoria}.",
                "Tarifas",
            )

            messages.success(
                self.request,
                "Tarifa eliminada correctamente.",
            )

            return response

        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar la tarifa porque está relacionada con paquetes.",
            )

            return redirect(self.success_url)