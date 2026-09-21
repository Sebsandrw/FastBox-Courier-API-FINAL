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

from .forms import ClienteForm
from .models import Cliente


class ClienteListView(ListView):
    model = Cliente
    template_name = "clientes/cliente_list.html"
    context_object_name = "clientes"
    paginate_by = 10

    extra_context = {
        "titulo_pagina": "Clientes",
    }


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy("clientes:cliente_lista")

    extra_context = {
        "titulo_pagina": "Registrar cliente",
        "texto_boton": "Guardar cliente",
    }

    def form_valid(self, form):
        response = super().form_valid(form)

        registrar_bitacora(
            self.request,
            "Cliente registrado",
            f"Se registró el cliente {self.object.nombres} {self.object.apellidos}.",
            "Clientes",
        )

        messages.success(
            self.request,
            "Cliente registrado correctamente.",
        )

        return response


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "clientes/cliente_detail.html"
    context_object_name = "cliente"

    extra_context = {
        "titulo_pagina": "Detalle del cliente",
    }


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy("clientes:cliente_lista")

    extra_context = {
        "titulo_pagina": "Editar cliente",
        "texto_boton": "Actualizar cliente",
    }

    def form_valid(self, form):
        response = super().form_valid(form)

        registrar_bitacora(
            self.request,
            "Cliente actualizado",
            f"Se actualizó la información del cliente {self.object.nombres} {self.object.apellidos}.",
            "Clientes",
        )

        messages.success(
            self.request,
            "Cliente actualizado correctamente.",
        )

        return response


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "clientes/cliente_confirm_delete.html"
    context_object_name = "cliente"
    success_url = reverse_lazy("clientes:cliente_lista")

    extra_context = {
        "titulo_pagina": "Eliminar cliente",
    }

    def form_valid(self, form):
        try:
            nombre_cliente = f"{self.object.nombres} {self.object.apellidos}"

            response = super().form_valid(form)

            registrar_bitacora(
                self.request,
                "Cliente eliminado",
                f"Se eliminó el cliente {nombre_cliente}.",
                "Clientes",
            )

            messages.success(
                self.request,
                "Cliente eliminado correctamente.",
            )

            return response

        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar el cliente porque tiene paquetes registrados.",
            )

            return redirect(self.success_url)