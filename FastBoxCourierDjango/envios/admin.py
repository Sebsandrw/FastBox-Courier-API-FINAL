from django.contrib import admin
from .models import MovimientoEnvio, Paquete

# Register your models here.
@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display =(
        "id_paquete",
        "guia_fastbox",
        "cliente",
        "tienda_origen",
        "peso_libras",
        "costo_estimado",
        "estado",
    )

    search_fields =(
        "guia_fastbox",
        "tracking_original",
        "descripcion",
        "cliente__nombres",
        "cliente__apellidos",
    )

    list_filter= (
        "estado",
        "tarifa",
    )

    list_select_related=(
        "cliente",
        "tarifa",
    )

    ordering=(
        "-fecha_registro",
    )

@admin.register(MovimientoEnvio)
class MovimientoEnvioAdmin(admin.ModelAdmin):
    list_display =(
        "id_movimiento",
        "paquete",
        "estado",
        "fecha_hora",
    )

    search_fields=(
        "paquete__guia_fastbox",
        "detalle",
    )

    list_filter=(
        "estado",
    )

    list_select_related=(
        "paquete",
    )

    ordering =(
        "-fecha_hora",
    )