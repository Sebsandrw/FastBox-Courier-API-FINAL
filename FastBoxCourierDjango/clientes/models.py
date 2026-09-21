# Create your models here.
from django.db import models

class Cliente(models.Model):
    id_cliente = models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    correo = models.EmailField(max_length=120, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=180, blank=True, null=True)

    # Código de casillero asignado al cliente.
    casillero = models.CharField(max_length=20, unique=True)

    estado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.casillero}"

    class Meta:
        db_table = "cliente"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["apellidos", "nombres"]
