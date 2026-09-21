from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente

        fields = [
            "nombres",
            "apellidos",
            "correo",
            "telefono",
            "direccion",
            "casillero",
            "estado",
        ]

        labels = {
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "correo": "Correo electrónico",
            "telefono": "Teléfono",
            "direccion": "Dirección",
            "casillero": "Código de casillero",
            "estado": "Cliente activo",
        }

        widgets = {
            "nombres": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. Sebastián",
                }
            ),
            "apellidos": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. Escobar",
                }
            ),
            "correo": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "cliente@correo.com",
                }
            ),
            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. 0999999999",
                }
            ),
            "direccion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. Guayaquil",
                }
            ),
            "casillero": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. FBX-SEB001",
                }
            ),
            "estado": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_nombres(self):
        nombres = self.cleaned_data.get("nombres", "")
        return nombres.strip()

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get("apellidos", "")
        return apellidos.strip()

    def clean_casillero(self):
        casillero = self.cleaned_data.get("casillero", "")
        return casillero.strip().upper()

    