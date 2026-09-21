from django.contrib import admin
from .models import Cliente
# Register your models here.

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display =(
        "id_cliente",
        "nombres",
        "apellidos",
        "correo",
        "casillero",
        "estado",
    )

    search_fields =(
        "nombres",
        "apellidos",
        "correo",
        "casillero",
    )

    list_filter= (
        "estado",
    )

    ordering=(
        "apellidos",
        "nombres",
    )