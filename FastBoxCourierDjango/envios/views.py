from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from bitacora.models import Bitacora
from clientes.models import Cliente
from tarifas.models import Tarifa

from bitacora.utils import registrar_bitacora

from .forms import MovimientoEnvioForm, PaqueteForm
from .models import MovimientoEnvio, Paquete

#dashboard seria la pantalla interfaz que cree para mostrar antes que las ventanas
@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_clientes"] = Cliente.objects.count()
        context["total_tarifas"] = Tarifa.objects.count()
        context["total_paquetes"] = Paquete.objects.count()
        context["total_movimientos"] = MovimientoEnvio.objects.count()

        context["ultimos_paquetes"] = (
            Paquete.objects
            .select_related("cliente", "tarifa")
            .order_by("-fecha_registro")[:5]
        )

        context["ultimas_acciones"] = (
            Bitacora.objects
            .order_by("-fecha_hora")[:5]
        )

        return context

class PaqueteListView(ListView):
    model = Paquete
    template_name = "envios/paquete_list.html"
    context_object_name = "paquetes"
    paginate_by = 10

    extra_context = {
        "titulo_pagina": "Paquetes",
    }

    def get_queryset(self):
        return (
            Paquete.objects
            .select_related("cliente", "tarifa")
            .order_by("-fecha_registro")
        )


class PaqueteCreateView(CreateView):
    model = Paquete
    form_class = PaqueteForm
    template_name = "envios/paquete_form.html"
    success_url = reverse_lazy("envios:paquete_lista")

    extra_context = {
        "titulo_pagina": "Registrar paquete",
        "texto_boton": "Guardar paquete",
    }

    def form_valid(self, form):
        response = super().form_valid(form)

        registrar_bitacora(
            self.request,
            "Paquete registrado",
            f"Se registró la guía {self.object.guia_fastbox}.",
            "Envíos",
        )

        messages.success(
            self.request,
            "Paquete registrado correctamente.",
        )

        return response


class PaqueteDetailView(DetailView):
    model = Paquete
    template_name = "envios/paquete_detail.html"
    context_object_name = "paquete"

    extra_context = {
        "titulo_pagina": "Detalle del paquete",
    }

    def get_queryset(self):
        return Paquete.objects.select_related("cliente", "tarifa")


class PaqueteUpdateView(UpdateView):
    model = Paquete
    form_class = PaqueteForm
    template_name = "envios/paquete_form.html"
    success_url = reverse_lazy("envios:paquete_lista")

    extra_context = {
        "titulo_pagina": "Editar paquete",
        "texto_boton": "Actualizar paquete",
    }

    def form_valid(self, form):
        response = super().form_valid(form)

        registrar_bitacora(
            self.request,
            "Paquete actualizado",
            f"Se actualizó la guía {self.object.guia_fastbox}.",
            "Envíos",
        )

        messages.success(
            self.request,
            "Paquete actualizado correctamente.",
        )

        return response


class PaqueteDeleteView(DeleteView):
    model = Paquete
    template_name = "envios/paquete_confirm_delete.html"
    context_object_name = "paquete"
    success_url = reverse_lazy("envios:paquete_lista")

    extra_context = {
        "titulo_pagina": "Eliminar paquete",
    }

    def form_valid(self, form):
        try:
            guia = self.object.guia_fastbox

            response = super().form_valid(form)

            registrar_bitacora(
                self.request,
                "Paquete eliminado",
                f"Se eliminó la guía {guia}.",
                "Envíos",
            )

            messages.success(
                self.request,
                "Paquete eliminado correctamente.",
            )

            return response

        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar el paquete porque tiene movimientos registrados.",
            )

            return redirect(self.success_url)


class MovimientoEnvioListView(ListView):
    model = MovimientoEnvio
    template_name = "envios/movimiento_list.html"
    context_object_name = "movimientos"
    paginate_by = 10

    extra_context = {
        "titulo_pagina": "Movimientos de envío",
    }

    def get_queryset(self):
        return (
            MovimientoEnvio.objects
            .select_related("paquete")
            .order_by("-fecha_hora")
        )


class MovimientoEnvioCreateView(CreateView):
    model = MovimientoEnvio
    form_class = MovimientoEnvioForm
    template_name = "envios/movimiento_form.html"
    success_url = reverse_lazy("envios:movimiento_lista")

    extra_context = {
        "titulo_pagina": "Registrar movimiento",
        "texto_boton": "Guardar movimiento",
    }

    def form_valid(self, form):
        response = super().form_valid(form)

        paquete = self.object.paquete
        paquete.estado = self.object.estado
        paquete.save()

        registrar_bitacora(
            self.request,
            "Movimiento registrado",
            f"La guía {paquete.guia_fastbox} cambió a {self.object.get_estado_display()}.",
            "Envíos",
        )

        messages.success(
            self.request,
            "Movimiento registrado correctamente.",
        )

        return response


class MovimientoEnvioDetailView(DetailView):
    model = MovimientoEnvio
    template_name = "envios/movimiento_detail.html"
    context_object_name = "movimiento"

    extra_context = {
        "titulo_pagina": "Detalle del movimiento",
    }

    def get_queryset(self):
        return MovimientoEnvio.objects.select_related("paquete")


class MovimientoEnvioUpdateView(UpdateView):
    model = MovimientoEnvio
    form_class = MovimientoEnvioForm
    template_name = "envios/movimiento_form.html"
    success_url = reverse_lazy("envios:movimiento_lista")

    extra_context = {
        "titulo_pagina": "Editar movimiento",
        "texto_boton": "Actualizar movimiento",
    }

    def form_valid(self, form):
        response = super().form_valid(form)

        paquete = self.object.paquete
        paquete.estado = self.object.estado
        paquete.save()

        registrar_bitacora(
            self.request,
            "Movimiento actualizado",
            f"Se actualizó un movimiento de la guía {paquete.guia_fastbox}.",
            "Envíos",
        )

        messages.success(
            self.request,
            "Movimiento actualizado correctamente.",
        )

        return response


class MovimientoEnvioDeleteView(DeleteView):
    model = MovimientoEnvio
    template_name = "envios/movimiento_confirm_delete.html"
    context_object_name = "movimiento"
    success_url = reverse_lazy("envios:movimiento_lista")

    extra_context = {
        "titulo_pagina": "Eliminar movimiento",
    }

    def form_valid(self, form):
        guia = self.object.paquete.guia_fastbox

        response = super().form_valid(form)

        registrar_bitacora(
            self.request,
            "Movimiento eliminado",
            f"Se eliminó un movimiento de la guía {guia}.",
            "Envíos",
        )

        messages.success(
            self.request,
            "Movimiento eliminado correctamente.",
        )

        return response
