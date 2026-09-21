# Create your models here.
from django.db import models

class Bitacora(models.Model):
    id_bitacora = models.BigAutoField(primary_key=True)

    fecha_hora = models.DateTimeField(auto_now_add=True)

    usuario = models.CharField(max_length=80)
    accion = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=220)
    modulo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.fecha_hora} - {self.accion}"

    class Meta:
        db_table = "bitacora"
        verbose_name = "Bitácora"
        verbose_name_plural = "Bitácora"
        ordering = ["-fecha_hora"]