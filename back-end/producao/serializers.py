from rest_framework import serializers

from cliente.models import Cliente
from pedido.models import Pedido
from usuario.models import Usuario
from .models import Producao

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'name']  # Adicione os campos necessários

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProducaoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    pedido = PedidoSerializer()
    cliente = ClienteSerializer()

    class Meta:
        model = Producao
        fields = '__all__'
