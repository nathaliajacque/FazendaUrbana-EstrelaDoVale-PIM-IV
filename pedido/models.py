"""
Campos da Classe PedidoVenda:

id_venda: Chave primária para identificar o pedido de venda.
num_pedido: Número do pedido.
status: Campo de escolha para o status do pedido.
data_venda: Data da venda.
data_cadastro: Data de cadastro do pedido (preenchida automaticamente).
usuario: Chave estrangeira para o usuário que criou o pedido.
cliente: Chave estrangeira para o cliente associado ao pedido.
prazo_entrega: Prazo de entrega do pedido.
Métodos da Classe PedidoVenda:

create_pedido_venda: Método de classe para criar um novo pedido de venda.
get_pedido_venda: Método de classe para obter um pedido de venda pelo ID.
update_pedido_venda: Método de classe para atualizar um pedido de venda.
concluir_pedido_venda: Método de instância para concluir um pedido de venda.
validar_dados: Método de instância para validar os dados do pedido.
cancelar_pedido_venda: Método de instância para cancelar um pedido de venda.
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import date
from cliente.models import Cliente
from produto.models import Produto
import os

# TODO: Fazer com que o pedido gere um prazo de acordo com o tempo de entrega do fornecedor + dias
# do crescimento do insumo


class PedidoVenda(models.Model):
    STATUS_CHOICES = [
        ("Em andamento", "Em andamento"),
        ("Concluído", "Concluído"),
        ("Cancelado", "Cancelado"),
    ]

    num_pedido = models.AutoField(primary_key=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Em andamento"
    )
    # adicionado total
    total = models.FloatField(default=1)
    data_venda = models.DateField()
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, editable=False
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=1)
    prazo_entrega = models.DateField()

    def __str__(self):
        return f"Pedido {self.num_pedido} - {self.cliente.nome}"

    @classmethod
    def create_pedido_venda(cls, **kwargs):
        pedido = cls(**kwargs)
        pedido.save()
        return pedido

    @classmethod
    def get_pedido_venda(cls, id_venda):
        try:
            pedido = cls.objects.get(id_venda=id_venda)
            return pedido
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_pedido_venda(cls, id_venda, **kwargs):
        try:
            pedido = cls.objects.get(id_venda=id_venda)
            for key, value in kwargs.items():
                setattr(pedido, key, value)
            pedido.save()
            return pedido
        except cls.DoesNotExist:
            return None

    def concluir_pedido_venda(self):
        self.status = "Em andamento"
        self.save()

    def concluir_pedido_venda(self):
        self.status = "Concluído"
        self.save()

    def cancelar_pedido_venda(self):
        self.status = "Cancelado"
        self.save()

    def validar_dados(self):
        # Adicione a lógica de validação aqui
        pass

    def __str__(self):
        return f"Pedido n° {self.num_pedido} - {self.cliente.nome}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class ItemPedido(models.Model):
    descricao = models.CharField(max_length=255)  # nome do produto
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)  # id do produto
    pedido = models.ForeignKey(PedidoVenda, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    pedido = models.ForeignKey(PedidoVenda, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.produto.descricao} - {self.quantidade} unidade(s)"

    @classmethod
    def create_item(cls, **kwargs):
        item = cls(**kwargs)
        item.save()
        return item

    @classmethod
    def get_item(cls, id_item):
        try:
            item = cls.objects.get(id_item=id_item)
            return item
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_item(cls, id_item, **kwargs):
        try:
            item = cls.objects.get(id_item=id_item)
            for key, value in kwargs.items():
                setattr(item, key, value)
            item.save()
            return item
        except cls.DoesNotExist:
            return None

    def calcular_valor_total(self):
        self.valor_total = self.quantidade * self.valor_unitario
        self.save()

    def __str__(self):
        return f"{self.produto.descricao} - {self.quantidade} unidade(s)"

    class Meta:
        verbose_name = "Item do pedido"
        verbose_name_plural = "Itens do pedido"
