
# Create your models here.
from django.db import models
class Tarifa(models.Model):

    class Categoria(models.TextChoices):
        TECNOLOGIA = "TECNOLOGIA", "Tecnología"
        ROPA = "ROPA", "Ropa"
        ACCESORIOS = "ACCESORIOS", "Accesorios"
        OTROS = "OTROS", "Otros"

    id_tarifa = models.BigAutoField(primary_key=True)

    categoria = models.CharField(
        max_length=20,
        choices=Categoria.choices,
        unique=True
    )

    valor_por_libra = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    descripcion = models.CharField(
        max_length=180,
        blank=True,
        null=True
    )

    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_categoria_display()} - ${self.valor_por_libra}"

    class Meta:
        db_table = "tarifa"
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"
        ordering = ["categoria"]