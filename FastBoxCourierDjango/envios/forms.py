from django import forms

from .models import MovimientoEnvio, Paquete


class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete

        fields = [
            "cliente",
            "tarifa",
            "guia_fastbox",
            "tracking_original",
            "tienda_origen",
            "descripcion",
            "peso_libras",
            "estado",
        ]

        labels = {
            "cliente": "Cliente",
            "tarifa": "Tarifa aplicada",
            "guia_fastbox": "Guía FastBox",
            "tracking_original": "Tracking original",
            "tienda_origen": "Tienda de origen",
            "descripcion": "Descripción del paquete",
            "peso_libras": "Peso en libras",
            "estado": "Estado del paquete",
        }

        widgets = {
            "cliente": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "tarifa": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "guia_fastbox": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. FBX-123456",
                }
            ),
            "tracking_original": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. 1Z999AA10123456784",
                }
            ),
            "tienda_origen": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. Amazon, Shein, eBay",
                }
            ),
            "descripcion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. Audífonos inalámbricos",
                }
            ),
            "peso_libras": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. 2.50",
                    "min": "0.01",
                    "step": "0.01",
                }
            ),
            "estado": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def clean_guia_fastbox(self):
        guia = self.cleaned_data.get("guia_fastbox", "")
        return guia.strip().upper()

    def clean_tracking_original(self):
        tracking = self.cleaned_data.get("tracking_original")

        if tracking:
            return tracking.strip().upper()

        return tracking

    def clean_peso_libras(self):
        peso = self.cleaned_data.get("peso_libras")

        if peso is not None and peso <= 0:
            raise forms.ValidationError(
                "El peso debe ser mayor a cero."
            )

        return peso


class MovimientoEnvioForm(forms.ModelForm):
    class Meta:
        model = MovimientoEnvio

        fields = [
            "paquete",
            "estado",
            "detalle",
        ]

        labels = {
            "paquete": "Paquete",
            "estado": "Estado",
            "detalle": "Detalle del movimiento",
        }

        widgets = {
            "paquete": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "estado": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "detalle": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. Paquete recibido en bodega de origen.",
                    "rows": 3,
                }
            ),
        }

    def clean_detalle(self):
        detalle = self.cleaned_data.get("detalle", "")
        return detalle.strip()