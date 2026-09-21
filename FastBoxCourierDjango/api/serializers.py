from rest_framework import serializers

from bitacora.models import Bitacora
from clientes.models import Cliente
from envios.models import MovimientoEnvio, Paquete
from tarifas.models import Tarifa


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            "id_cliente",
            "nombres",
            "apellidos",
            "correo",
            "telefono",
            "direccion",
            "casillero",
            "estado",
            "fecha_registro",
        ]


class TarifaSerializer(serializers.ModelSerializer):
    categoria_texto = serializers.CharField(
        source="get_categoria_display",
        read_only=True,
    )

    class Meta:
        model = Tarifa
        fields = [
            "id_tarifa",
            "categoria",
            "categoria_texto",
            "valor_por_libra",
            "descripcion",
            "estado",
        ]


class PaqueteSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.SerializerMethodField()
    cliente_casillero = serializers.CharField(
        source="cliente.casillero",
        read_only=True,
    )
    tarifa_categoria = serializers.CharField(
        source="tarifa.get_categoria_display",
        read_only=True,
    )
    estado_texto = serializers.CharField(
        source="get_estado_display",
        read_only=True,
    )

    class Meta:
        model = Paquete
        fields = [
            "id_paquete",
            "cliente",
            "cliente_nombre",
            "cliente_casillero",
            "tarifa",
            "tarifa_categoria",
            "guia_fastbox",
            "tracking_original",
            "tienda_origen",
            "descripcion",
            "peso_libras",
            "costo_estimado",
            "estado",
            "estado_texto",
            "fecha_registro",
            "fecha_actualizacion",
        ]

        read_only_fields = [
            "costo_estimado",
            "fecha_registro",
            "fecha_actualizacion",
        ]

    def get_cliente_nombre(self, obj):
        return f"{obj.cliente.nombres} {obj.cliente.apellidos}"


class MovimientoEnvioSerializer(serializers.ModelSerializer):
    paquete_guia = serializers.CharField(
        source="paquete.guia_fastbox",
        read_only=True,
    )
    estado_texto = serializers.CharField(
        source="get_estado_display",
        read_only=True,
    )

    class Meta:
        model = MovimientoEnvio
        fields = [
            "id_movimiento",
            "paquete",
            "paquete_guia",
            "estado",
            "estado_texto",
            "detalle",
            "fecha_hora",
        ]

        read_only_fields = [
            "fecha_hora",
        ]


class BitacoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitacora
        fields = [
            "id_bitacora",
            "fecha_hora",
            "usuario",
            "accion",
            "descripcion",
            "modulo",
        ]