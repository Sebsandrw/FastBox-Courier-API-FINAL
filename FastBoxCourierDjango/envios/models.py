# Create your models here.
from django.db import models

from clientes.models import Cliente
from tarifas.models import Tarifa

class Paquete(models.Model):

    class EstadoPaquete(models.TextChoices):
        PREALERTA = "PREALERTA", "Prealerta registrada"
        BODEGA = "BODEGA", "Recibido en bodega"
        TRANSITO = "TRANSITO", "En tránsito"
        ECUADOR = "ECUADOR", "Llegó a Ecuador"
        ENTREGA = "ENTREGA", "Listo para entrega"
        ENTREGADO = "ENTREGADO", "Entregado"

    id_paquete = models.BigAutoField(primary_key=True)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="paquetes"
    )

    tarifa = models.ForeignKey(
        Tarifa,
        on_delete=models.PROTECT,
        related_name="paquetes"
    )

    guia_fastbox = models.CharField(max_length=20, unique=True)

    tracking_original = models.CharField(
        max_length=60,
        blank=True,
        null=True
    )

    tienda_origen = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=180)

    peso_libras = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    costo_estimado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    estado = models.CharField(
        max_length=20,
        choices=EstadoPaquete.choices,
        default=EstadoPaquete.PREALERTA
    )

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # Calcula el costo del paquete antes de guardar.
    def save(self, *args, **kwargs):
        if self.tarifa and self.peso_libras:
            self.costo_estimado = (
                self.peso_libras * self.tarifa.valor_por_libra
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guia_fastbox} - {self.descripcion}"

    class Meta:
        db_table = "paquete"
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes"
        ordering = ["-fecha_registro"]


class MovimientoEnvio(models.Model):
    id_movimiento = models.BigAutoField(primary_key=True)

    paquete = models.ForeignKey(
        Paquete,
        on_delete=models.PROTECT,
        related_name="movimientos"
    )

    estado = models.CharField(
        max_length=20,
        choices=Paquete.EstadoPaquete.choices
    )

    detalle = models.CharField(max_length=200)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.paquete.guia_fastbox} - {self.get_estado_display()}"

    class Meta:
        db_table = "movimiento_envio"
        verbose_name = "Movimiento de envío"
        verbose_name_plural = "Movimientos de envío"
        ordering = ["-fecha_hora"]

