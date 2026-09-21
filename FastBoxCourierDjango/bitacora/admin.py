from django.contrib import admin
from .models import Bitacora

# Register your models here.
@admin.register(Bitacora)
class BitacoraAdmin(admin.ModelAdmin):
    list_display =(
            "id_bitacora",
            "fecha_hora",
            "usuario",
            "accion",
            "modulo",

        )
    
    search_fields =(
            "usuario",
            "accion",
            "descripcion",
            "modulo",
        )
    
    list_filter= (
            "modulo",
            "accion",
        )
    
    ordering=(
            "-fecha_hora",
        )

    #bitacora queda como registro de consulta

    def has_delete_permission(self, request, obj = None):
        return False