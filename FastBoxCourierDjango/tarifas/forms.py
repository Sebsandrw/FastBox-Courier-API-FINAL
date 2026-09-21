from django import forms
from .models import Tarifa

class TarifaForm(forms.ModelForm):
    class Meta:
        model = Tarifa

        fields = [
            "categoria",
            "valor_por_libra",
            "descripcion",
            "estado",
        ]

        labels = {
            "categoria": "Categoría",
            "valor_por_libra": "Valor por libra",
            "descripcion": "Descripción",
            "estado": "Tarifa activa",
        }

        widgets = {
            "categoria": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "valor_por_libra": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. 5.50",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Detalle breve de la tarifa",
                    "rows": 3,
                }
            ),
            "estado": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_valor_por_libra(self):
        valor = self.cleaned_data.get("valor_por_libra")

        if valor is not None and valor < 0:
            raise forms.ValidationError(
                "El valor por libra no puede ser negativo."
            )

        return valor