from django.contrib import admin
from .models import Tarifa

# Register your models here.
@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display =(
        "id_tarifa",
        "categoria",
        "valor_por_libra",
        "estado",
    )

    search_fields =(
        "categoria",
        "descripcion",
    )

    list_filter= (
        "categoria",
        "estado",
    )

    ordering=(
        "categoria",
    )